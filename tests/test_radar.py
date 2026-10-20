import json
import unittest
from datetime import timedelta
from unittest.mock import patch

from main import (
    make_item, normalize_link, rule_enrich, esc, utc_now, months_ago,
    date_in_window, crossref_date, openalex_abstract, identity_key,
    deduplicate_items, fetch_arxiv_api, fetch_openalex, fetch_crossref, render_html, get_focus,
    select_arxiv_queries, request_with_retry, historical_backfill_jobs, annual_backfill_jobs, classify_primary_topic, rotate_source_queries
)

class FakeResponse:
    def __init__(self, data=None, body=None):
        self._data = data
        self.content = body or b''
    def raise_for_status(self):
        pass
    def json(self):
        return self._data

class RadarTests(unittest.TestCase):
    def test_normalize_url(self):
        self.assertEqual(normalize_link('https://example.org/a/#f'), 'https://example.org/a')

    def test_classify_brain(self):
        item = make_item('Agentic VLN navigation', 'https://example.org/a', 'arXiv',
                         '论文（摘要）', 'vision-language models call skills for robot navigation')
        classified = rule_enrich(item)
        self.assertIsNotNone(classified)
        self.assertIn('大脑与具身智能', classified['tags'])

    def test_historical_arxiv_api_disabled_by_default(self):
        cfg = {"arxiv_queries": ["a", "b", "c"]}
        self.assertEqual(select_arxiv_queries(cfg), [])
        cfg["arxiv_queries_per_run"] = 1
        self.assertEqual(len(select_arxiv_queries(cfg)), 1)
        cfg["arxiv_queries_per_run"] = 9
        self.assertEqual(set(select_arxiv_queries(cfg)), {"a", "b", "c"})

    def test_source_warning_is_collapsible(self):
        cfg = {"history_months": 6, "display_limit": 500, "industry_watchlist": []}
        html_text = render_html([], ["OpenAlex: HTTP 504"], cfg)
        self.assertIn('class="source-status"', html_text)
        self.assertIn("weekly.md", html_text)
        self.assertNotIn("本次采集部分失败", html_text)

    @patch("main.time.sleep")
    @patch("requests.get")
    def test_openalex_retry_on_504(self, mock_get, mock_sleep):
        class Response:
            headers = {}
            def __init__(self, status):
                self.status_code = status
            def raise_for_status(self):
                if self.status_code >= 400:
                    raise __import__("requests").HTTPError(str(self.status_code))
        mock_get.side_effect = [Response(504), Response(200)]
        response = request_with_retry("https://example.org/api", attempts=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once()

    @patch("main.time.sleep")
    @patch("requests.get")
    def test_no_retry_for_429_without_retry_after(self, mock_get, mock_sleep):
        class Response:
            status_code = 429
            headers = {}
            def raise_for_status(self):
                raise __import__("requests").HTTPError("429 rate limited")
        mock_get.return_value = Response()
        with self.assertRaises(__import__("requests").HTTPError):
            request_with_retry("https://example.org/api", attempts=3)
        mock_get.assert_called_once()
        mock_sleep.assert_not_called()

    def test_html_escape(self):
        self.assertEqual(esc('<script>'), '&lt;script&gt;')

    def test_six_calendar_months(self):
        dt = months_ago(6)
        self.assertEqual(dt.hour, 0)
        self.assertEqual(dt.minute, 0)
        self.assertTrue(179 <= (utc_now() - dt).days <= 186)

    def test_crossref_published_date(self):
        w = {'published-online': {'date-parts': [[2026, 9, 15]]}}
        self.assertEqual(crossref_date(w), '2026-09-15')

    def test_abstract_inverted_index(self):
        self.assertEqual(openalex_abstract({'robot': [0], 'navigation': [1]}), 'robot navigation')

    def test_deduplicate_by_title(self):
        x = make_item('Learning Robot Navigation!', 'https://arxiv.org/abs/1234',
                      'arXiv API', '论文（摘要）', 'robot navigation models')
        y = make_item('Learning Robot Navigation', 'https://doi.org/10.123/a',
                      'OpenAlex', '论文（摘要）', 'robot navigation models with language and memory')
        out = deduplicate_items([x, y])
        self.assertEqual(len(out), 1)
        self.assertIn('memory', out[0]['description'])

    @patch('requests.get')
    def test_arxiv_api_parse(self, mock_get):
        body = b'''<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
          <entry><id>https://arxiv.org/abs/2609.00123</id><title>Robot navigation</title>
          <summary>Vision language robot agent</summary><published>2026-09-10T00:00:00Z</published></entry>
          </feed>'''
        mock_get.return_value = FakeResponse(body=body)
        start = utc_now().replace(year=2026, month=4, day=1)
        end = utc_now().replace(year=2026, month=10, day=12)
        out = fetch_arxiv_api('all:robot', start, end)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]['source'], 'arXiv API')
        self.assertIn('submittedDate:', mock_get.call_args.kwargs['params']['search_query'])

    @patch('requests.get')
    def test_openalex_parse(self, mock_get):
        mock_get.return_value = FakeResponse(data={'results': [
            {'display_name': 'Robot Agentic Navigation', 'publication_date': '2026-09-03',
             'type': 'article', 'doi': 'https://doi.org/10.9999/example',
             'abstract_inverted_index': {'agentic': [0], 'robot': [1], 'navigation': [2]},
             'primary_location': {'source': {'display_name': 'Robotics Journal'}}}
        ]})
        start = utc_now().replace(year=2026, month=4, day=1)
        end = utc_now().replace(year=2026, month=10, day=12)
        out = fetch_openalex('robot agent', start, end)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]['source'], 'OpenAlex')

    @patch('requests.get')
    def test_crossref_parse(self, mock_get):
        mock_get.return_value = FakeResponse(data={'message': {'items': [
            {'type': 'journal-article', 'title': ['Quadruped Robot Control'],
             'DOI': '10.3333/example', 'published': {'date-parts': [[2026, 8, 1]]},
             'container-title': ['Journal X']}
        ]}})
        start = utc_now().replace(year=2026, month=4, day=1)
        end = utc_now().replace(year=2026, month=10, day=12)
        out = fetch_crossref('quadruped', start, end)
        self.assertEqual(len(out), 1)
        self.assertTrue(out[0]['url'].startswith('https://doi.org/'))

    def test_backfill_spans_older_quarters(self):
        from datetime import datetime, timezone
        now = datetime(2026, 10, 15, tzinfo=timezone.utc)
        jobs = historical_backfill_jobs(["quadruped robot", "robot navigation"], now, 24, 3, 8)
        self.assertEqual(len(jobs), 8)
        self.assertTrue(all(s < e <= now for _, s, e in jobs))
        self.assertTrue(any(s.year <= 2025 for _, s, e in jobs))

    def test_two_year_date_filter_ui(self):
        from datetime import datetime, timezone
        cfg = {'history_months': 24, 'display_limit': 5000, 'industry_watchlist': []}
        record = make_item('Robot navigation', 'https://example.org/paper', 'OpenAlex',
                           '论文（摘要）', 'robot navigation system', '2025-01-01')
        record['category'] = '感知建图与导航'
        record['tags'] = ['感知建图与导航']
        record['score'] = 80
        output = render_html([record], [], cfg)
        self.assertIn('id="fromDate"', output)
        self.assertIn('id="toDate"', output)
        self.assertIn('data-date="2025-01-01"', output)
        self.assertIn('data-preset="365"', output)
        self.assertIn('data-preset="all"', output)
        self.assertIn('研究成果与开源项目', output)

    def test_hardware_recall_real_database_cases(self):
        cases = [
            ("Design and Development of Explosion-Proof Cavity of Hydraulic System Power Unit Applied in Explosion-Proof Area",
             "The explosion-proof housing of hydraulic system power unit is investigated.", "硬件与防爆"),
            ("Research on Inspection Technology of Limited-rotation Explosion-proof Electric Actuators for Coal Mines",
             "The composition structure of the explosion-proof limited-angle electric actuator is investigated.", "硬件与防爆"),
            ("Influence of periodic pulse intake on the ventilation efficiency of positive pressure explosion-proof robot",
             "The robot positive pressure explosion-proof structure and periodic purge ventilation method are studied.", "硬件与防爆"),
            ("A Low-Cost, Open-Source Quadruped Robot for Assistive Elder Care: Design, Implementation, and Validation",
             "This article presents design fabrication mechanical chassis and a printed circuit board with servo motors.", "硬件与防爆"),
            ("Quadruped Locomotion via Reinforcement Learning under Actuator Failures",
             "Residual control using joint encoders and sensors.", "小脑与运动控制"),
            ("LiDAR-Based Robot Navigation Using Actuator Constraints",
             "Autonomous path planning and obstacle avoidance.", "感知建图与导航"),
        ]
        for title, abstract, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_primary_topic(title, abstract)[0], expected)

    def test_hardware_query_rotation(self):
        from datetime import datetime, timezone, timedelta
        today = datetime(2026, 10, 15, tzinfo=timezone.utc)
        q = ["a", "b", "c", "d", "e"]
        out = rotate_source_queries(q, 2, today)
        self.assertEqual(len(out), 2)
        self.assertTrue(set(out).issubset(q))
        self.assertEqual(rotate_source_queries(q, 0, today), [])
        self.assertNotEqual(out, rotate_source_queries(q, 2, today + timedelta(days=1)))

    def test_reject_nontechnical_posts(self):
        from taxonomy import is_non_technical
        for title in [
            'Robotics Prototyping Intern @ Nestack Technologies in Hyderabad, India (On-site)',
            'Boston Robot Hackers meeting Oct 15 at 7:00. Read for details',
            'Community meeting: Scalable Multi-Robot Simulation in ROS 2 and Gazebo',
        ]:
            with self.subTest(title=title):
                item = make_item(title, 'https://example.org/' + str(len(title)),
                                 'ROS Discourse', '社区动态',
                                 'robot navigation reinforcement learning ros2')
                self.assertTrue(is_non_technical(item)[0])
                self.assertIsNone(rule_enrich(item))
        paper = make_item('ROS 2 QoS for real-time quadruped control',
                          'https://example.org/paper', 'OpenAlex', '论文（摘要）',
                          'Meeting safety requirements for robot motion control.')
        self.assertFalse(is_non_technical(paper)[0])

    def test_second_round_actual_misclassifications(self):
        from taxonomy import classify_contribution
        cases = [
            ("A Multi-Scale Structured Exploration Mechanism for Deep Reinforcement Learning in Quadruped Robot Control", "小脑与运动控制"),
            ("A hierarchical QP optimization control strategy for quadruped robots facing a variety of structural terrains", "小脑与运动控制"),
            ("Research on Motion Control Method of Wheel-Legged Robot in Unstructured Terrain Based on Improved Central Pattern Generator (CPG) and Biological Reflex Mechanism", "小脑与运动控制"),
            ("A task level fusion autonomous switching mechanism", "感知建图与导航"),
            ("Transforming a Quadruped into a Guide Robot for the Visually Impaired: Formalizing Wayfinding, Interaction Modeling, and Safety Mechanism", "感知建图与导航"),
            ("A Paragraph is All It Takes: Rich Robot Behaviors from Interacting, Trusted LLMs", "大脑与具身智能"),
            ("Design and Testing of Two Haptic Devices Based on Reconfigurable 2R Joints", "硬件与防爆"),
            ("TAIL: A Terrain-Aware Multi-Modal SLAM Dataset for Robot Locomotion in Deformable Granular Environments", "基础软件与系统"),
            ("A Quadruped Piezoelectric Ultrasonic Actuating Robot with Foot-Leg-Trunk-Integrated Structure", "硬件与防爆"),
            ("SLAMs for Quadruped Robot: Mapping Capability-centric Agentic Simulation", "基础软件与系统"),
            ("Exploring Nonlinear Body Oscillations for Natural Quadruped Gaits", "小脑与运动控制"),
            ("Teaching a Robot Dog New Tricks: Diverse Quadruped Skills via Combined Reinforcement and Imitation Learning with Adversarial Task Selection", "小脑与运动控制"),
            ("QuadrupedGPT: Towards a Versatile Quadruped Agent in Open-ended Worlds", "大脑与具身智能"),
            ("Active Exploration in Bayesian Model-based Reinforcement Learning for Robot Manipulation", "小脑与运动控制"),
            ("Design and Characterization of a Unified Continuum Robot Actuation Platform", "硬件与防爆"),
            ("ProWorld: Multi-View World Model with Proprioceptive Feedback for Closed-Loop Policy Evaluation", "大脑与具身智能"),
            ("Mode-Reactive Template-Based Control in Planar Legged Robots", "小脑与运动控制"),
            ("Strategies for Generating Footsteps of Biped Robots in Narrow Sight", "小脑与运动控制"),
        ]
        for title, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_contribution(title).category, expected)

    def test_nontechnical_scope_exclusions(self):
        from taxonomy import is_non_technical
        for title in [
            "Research on and Design of an Electric Drive Automatic Control System for Mine Belt Conveyors",
            "How Does Exposure to Changing Opinions or Reaffirmation Opinions Influence the Thoughts of Observers and Their Trust in Robot Discussions?"
        ]:
            with self.subTest(title=title):
                self.assertTrue(is_non_technical({"title": title, "source": "OpenAlex"})[0])

    def test_ambiguous_mechanism_is_not_hardware(self):
        from taxonomy import classify_contribution
        for title in [
            "Reinforcement Learning Exploration Mechanism for Quadruped Control",
            "Biological Reflex Mechanism for Wheel-Legged Motion Control",
            "Safety Mechanism for Mobile Robot Navigation"
        ]:
            self.assertNotEqual(classify_contribution(title).category, "硬件与防爆")

    def test_hardware_primary_deliverable_boundaries(self):
        from taxonomy import classify_contribution
        examples = [
            ("Machine learning techniques for robotic and autonomous inspection of mechanical systems and civil infrastructure",
             "The review analyzes machine learning for planning, navigation and machine vision.", "感知建图与导航", True),
            ("Development of Delta Robot Arm Simulation in ROS2 Foxy Fitzroy Environment",
             "CAD models are converted to SDF and tested in Gazebo.", "基础软件与系统", False),
            ("Design of a Parallel Quadruped Robot Based on a Novel Intelligent Control System",
             "A novel intelligent controller was designed. Cascade PID and fuzzy adaptive PID are used for gait tracking.",
             "小脑与运动控制", True),
            ("Development of a Mobile Robot Platform for Smart Warehouse Management System",
             "Existing TurtleBot3 Waffle Pi integration for warehouse logistics.",
             "特种应用与产品", True),
            ("Kinematic Design and Dimensional Synthesis of a Symmetric Five-bar Wheel-leg Mechanism",
             "A new mechanical linkage and geometry synthesis for lifting.", "硬件与防爆", False),
            ("Design and Development of Explosion-Proof Cavity of Hydraulic System Power Unit",
             "Flameproof housing, mechanical design, test and safety.", "硬件与防爆", False),
            ("A low backlash and highly efficient gearbox for robot actuator",
             "Precision reducer transmission development.", "硬件与防爆", False),
            ("Robust design of a conformal adaptive foot for quadruped robots",
             "An adaptive foot structure and mechanical contact experiments.", "硬件与防爆", False),
            ("Design and Analysis of a Quadruped Wheel-Legged Robot Based on Virtual Equivalent Parallel Mechanism Theory",
             "Kinematic synthesis of a new leg mechanism.", "硬件与防爆", False),
            ("Quadruped locomotion with reinforcement learning and actuator constraints",
             "A locomotion policy uses existing robot motors.", "小脑与运动控制", False),
        ]
        for title, abstract, category, review in examples:
            with self.subTest(title=title):
                got=classify_contribution(title, abstract)
                self.assertEqual(got.category, category)
                self.assertEqual(got.review, review)

    def test_embodied_agent_recall_without_navigation_contamination(self):
        from taxonomy import classify_contribution
        cases = [
            ("BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation", "Deploying language-model agents requires task reasoning, behavior-tree skills and failure feedback.", "大脑与具身智能"),
            ("CAMON: Cooperative Agents for Multi-Object Navigation with LLM-based Conversations", "Cooperative robot agents use LLM conversations for planning.", "大脑与具身智能"),
            ("VIA: Visual Interface Agent for Robot Control", "Off-the-shelf foundation model powered agent performs task planning through an interface.", "大脑与具身智能"),
            ("ASENA: Self-evolving Agents for Embodied Navigation", "Robot agent calls tools and executes skills.", "大脑与具身智能"),
            ("Fast-VLA: You Only Think Once for Robot Manipulation", "A vision-language-action model uses a frozen VLM to build task context memory.", "大脑与具身智能"),
            ("CLASH: Collaborative Large-Small Hierarchical Framework for Continuous Vision-and-Language Navigation", "Reflective large-model reasoner and small-model reactive planner cooperate.", "大脑与具身智能"),
            ("DeCoNav: Dialog enhanced Long-Horizon Collaborative Vision-Language Navigation", "Multi-robot dialog and cooperative reasoning.", "大脑与具身智能"),
            ("ZeST: A VLM-based Zero-Shot Traversability Navigation for Unknown Environments", "Uses a VLM to measure terrain traversability and infer a posterior.", "感知建图与导航"),
            ("SLAM with Multi-Agent Reinforcement Learning for Quadruped Navigation", "An RL-based low-level controller.", "感知建图与导航"),
            ("Multi-Agent Reinforcement Learning for Quadruped Locomotion", "Walking via policy learning.", "小脑与运动控制"),
            ("JitterVLA: A Replay Benchmark for Motion Quality in VLA-Driven Manipulation", "Benchmark comparing controllers.", "基础软件与系统"),
        ]
        for title, abstract, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_contribution(title, abstract).category, expected)

    def test_embodied_queries_reserved_in_config(self):
        from backfill import backfill_queue
        from datetime import datetime, timezone
        from pathlib import Path
        cfg=json.loads(Path("config.json").read_text())
        self.assertTrue(cfg["brain_openalex_queries"])
        self.assertTrue(cfg["brain_archive_openalex_queries"])
        b=dict(cfg)
        b["archive_openalex_queries"]=cfg["brain_archive_openalex_queries"]
        queue=backfill_queue(b, datetime(2026,10,19,tzinfo=timezone.utc), {}, "OpenAlex")
        self.assertGreater(len(queue),20)
        self.assertEqual(len(queue),len(set(j[0] for j in queue)))

    def test_primary_contribution_misclassification_regressions(self):
        from taxonomy import classify_contribution
        examples = [
            ('PanoPed: Beyond Bounding Boxes for Sim-to-Real Panoramic Pedestrian Tracking', '感知建图与导航'),
            ('Robust design of a conformal adaptive foot for quadruped robots', '硬件与防爆'),
            ('Design and evaluation of a bio-inspired tendon-driven continuum robotic spine for quadruped applications', '硬件与防爆'),
            ('Origaker: A Novel Multi-Mimicry Quadruped Robot Based on a Metamorphic Mechanism', '硬件与防爆'),
            ('Adaptive mapless mobile robot navigation using deep reinforcement learning based improved TD3 algorithm', '感知建图与导航'),
            ('Deep Reinforcement Learning for Mobile Robot Navigation in Indoor Environments', '感知建图与导航'),
            ('ASENA: Self-evolving Agents for Embodied Navigation', '大脑与具身智能'),
            ('PILOT: Guiding Long-Horizon World-Model Planning for Robot Manipulation with Visual Subgoals and Policy Priors', '大脑与具身智能'),
            ('SharedKV-BT: Node-Local Typed Decisions for Behavior-Tree Agents', '大脑与具身智能'),
            ('Whole-Body Motion Response to Abrupt Acceleration Changes: Rapid CoM Motion Mapping, Compensation and Tracking for Wheel-Legged Humanoid Robot', '小脑与运动控制'),
            ('Adaptive Motion Skill Learning of Quadruped Robot on Slopes Based on Augmented Random Search Algorithm', '小脑与运动控制'),
            ('Recent advances in Rapidly-exploring random tree: A review', '感知建图与导航'),
            ('3D Printed Drivetrain Development for Inspection Robot', '硬件与防爆'),
            ('Cable management design for Inspection Robot', '硬件与防爆'),
            ('Dynamic target tracking algorithm for substation inspection robot', '感知建图与导航'),
            ('Force-Modulated Dexterity: Unified Compliance for Contact-Rich Manipulation', '小脑与运动控制'),
            ('Human2Dex: Dexterous Robot Learning from Wrist-Centric Human Demonstrations', '小脑与运动控制'),
            ('Comparison of ROS 2 QoS Policies for Real-Time Quadruped Robot Control', '基础软件与系统'),
            ('Robot locomotion via reinforcement learning under actuator failures', '小脑与运动控制'),
            ('LiDAR-based mobile robot navigation using a camera and motor commands', '感知建图与导航'),
            ('Explosion-Proof Motor and Flameproof Enclosure Design', '硬件与防爆'),
        ]
        for title, category in examples:
            with self.subTest(title=title):
                self.assertEqual(classify_contribution(title).category, category)

    def test_review_flag_and_no_default_trusted_app(self):
        from taxonomy import classify_contribution
        x = classify_contribution('A multi-robot study', '')
        self.assertTrue(x.review)
        self.assertEqual(x.confidence, '待复核')

    def test_primary_category_prevents_hardware_false_positives(self):
        cases = [
            ("Quadruped locomotion with reinforcement learning and sensor failures", "Online residual policy recovers from actuator faults", "小脑与运动控制"),
            ("Smoothed-PRM-Guided NMPC for Wheeled Mobile Robot Navigation", "Path planning with actuator constraints", "感知建图与导航"),
            ("LiDAR-Based Navigation System for an Autonomous Mobile Robot", "Robot with sensors and actuators", "感知建图与导航"),
            ("Visual-Inertial Odometry for Mobile Robots", "Dedicated hardware sensors and wheel encoders", "感知建图与导航"),
            ("Explosion-Proof Motor and Flameproof Enclosure Design", "Motor and enclosure engineering", "硬件与防爆"),
            ("Design of a Wheel-Legged Robot Joint Actuator", "Robot actuator design and mechanical transmission", "硬件与防爆"),
            ("Robot Agentic Task Planning with Vision Language Models", "Robot navigation with skill calling", "大脑与具身智能"),
            ("ROS 2 Simulation Platform for Robot Testing", "Gazebo and middleware architecture", "基础软件与系统"),
        ]
        for title, desc, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_primary_topic(title, desc)[0], expected)

    def test_persistent_archive_half_year_queue(self):
        from datetime import datetime, timezone
        from backfill import historical_windows, backfill_queue
        now = datetime(2026, 10, 15, tzinfo=timezone.utc)
        windows = historical_windows(now, 60)
        self.assertEqual(len(windows), 9)
        self.assertEqual(sorted(set(s.year for s, _ in windows)), [2021,2022,2023,2024,2025])
        config = {"history_months": 60, "archive_openalex_queries": ["quadruped", "slam"]}
        jobs = backfill_queue(config, now, {}, "OpenAlex")
        self.assertEqual(len(jobs), 18)
        marked = {jobs[0][0]: now.isoformat()}
        second = backfill_queue(config, now, marked, "OpenAlex")
        self.assertEqual(len(second), 17)
        self.assertNotIn(jobs[0][0], [j[0] for j in second])

    def test_annual_backfill_coverage(self):
        from datetime import datetime, timezone, timedelta
        now=datetime(2026, 10, 15, tzinfo=timezone.utc)
        years=set()
        for day in range(10):
            for _, start, end in annual_backfill_jobs(["robot", "quadruped"], now+timedelta(days=day), 60, daily_budget=3):
                years.add(start.year)
                self.assertLessEqual(start, end)
                self.assertLessEqual(end, now+timedelta(days=day))
        self.assertTrue({2021,2022,2023,2024,2025,2026}.issubset(years))

    def test_pagination_ten_and_jump_controls(self):
        import json
        cfg=json.loads(__import__('pathlib').Path('config.json').read_text())
        self.assertEqual(cfg['page_size'], 10)
        html_text=render_html([],[],cfg)
        for token in ['id="firstPage"', 'id="lastPage"', 'id="jumpPage"', 'id="jumpButton"', 'const PAGE_SIZE = 10;', '%%YEAR_STATS%%']:
            if token=='%%YEAR_STATS%%':
                self.assertNotIn(token,html_text)
            else:
                self.assertIn(token,html_text)

    def test_five_year_time_window(self):
        cfg = {'history_months': 60, 'display_limit': 15000, 'industry_watchlist': []}
        out = render_html([], [], cfg)
        self.assertIn('近五年', out)
        self.assertIn('全部五年', out)
        self.assertIn('data-preset="1095"', out)

    def test_render_500_limit(self):
        from main import utc_now
        cfg = {'history_months': 6, 'display_limit': 500, 'industry_watchlist': []}
        items = []
        for i in range(530):
            z = make_item(f'Quadruped locomotion research {i}', f'https://example.org/{i}',
                          'arXiv API', '论文（摘要）', 'robot locomotion', utc_now().isoformat())
            z['category'] = '小脑与运动控制'; z['tags'] = ['小脑与运动控制']; z['score'] = 60
            items.append(z)
        html_text = render_html(items, [], cfg)
        self.assertEqual(html_text.count('<article class="card"'), 500)

    def test_omit_generic_ai_and_non_robot_motor(self):
        for title, desc in [
            ('Large language models for financial trading', 'agentic tool calling using memory'),
            ('Novel electric motor for consumer vehicles', 'high performance motor drive and battery'),
            ('Industrial inspection via satellite imaging', 'deep learning for oil and gas'),
            ('Medical image segmentation with VLM', 'vision language models and RL'),
        ]:
            item = make_item(title, 'https://example.org/' + str(len(title)), 'OpenAlex',
                             '论文（摘要）', desc)
            self.assertIsNone(rule_enrich(item), title)

    def test_accept_direct_special_robots(self):
        examples = [
            ('Explosion proof quadruped robot', 'Robotic inspection in hazardous petrochemical plants', '防爆石化与危险环境'),
            ('Firefighting robot navigation', 'Autonomous search and rescue robotics', '消防与应急救援'),
            ('Inspection robot in coal mines', 'Mining robot localization and mapping', '矿山与地下空间'),
        ]
        for title, desc, scenario in examples:
            item = make_item(title, 'https://example.org/' + str(len(title)), 'arXiv API',
                             '论文（摘要）', desc)
            out = rule_enrich(item)
            self.assertIsNotNone(out)
            self.assertEqual(out['scope'], '特种场景直接相关')
            self.assertIn(scenario, out['industry_tags'])

    def test_keep_robot_native_tech_but_not_generic_ai(self):
        examples = [
            ('Quadruped robot locomotion', 'Whole body control and reinforcement learning', '小脑与运动控制'),
            ('Mobile robot agentic VLN', 'Robot navigation with skill library and tool calling', '大脑与具身智能'),
            ('ROS2 for robotic autonomy', 'Robot middleware system architecture and sensors', '基础软件与系统'),
            ('Robot actuator design', 'High-torque joint actuator and motor drive for robots', '硬件与防爆'),
        ]
        for title, desc, category in examples:
            item = make_item(title, 'https://example.org/' + str(len(title)), 'OpenAlex',
                             '论文（摘要）', desc)
            out = rule_enrich(item)
            self.assertIsNotNone(out, title)
            self.assertEqual(out['scope'], '可迁移的机器人关键技术')
            self.assertEqual(out['category'], category)

    def test_agentic_skill_navigation_not_hidden_by_perception(self):
        from taxonomy import classify_contribution
        cases = [
            ("Vision Language Navigation with Robot Agent Skill Calling",
             "The VLM agent performs task decomposition and selects navigation skills."),
            ("Embodied Agent for Autonomous Navigation",
             "An LLM performs high level task planning and tool calling for robot navigation."),
        ]
        for title, desc in cases:
            with self.subTest(title=title):
                got = classify_contribution(title, desc)
                self.assertEqual(got.category, '大脑与具身智能')

    def test_github_resource_indexes_are_not_original_technical_outputs(self):
        from taxonomy import is_non_technical
        for title in ['researcher/Awesome-Dexterous-Manipulation',
                      'robotuser/robotuser', 'lab/reading-list-robotics']:
            rejected, reason = is_non_technical(
                {'title': title, 'source': 'GitHub', 'type': '开源项目'})
            self.assertTrue(rejected, (title, reason))
        self.assertFalse(is_non_technical(
            {'title': 'robotlab/robot-navigation-stack', 'source': 'GitHub'})[0])

    def test_application_algorithm_boundary_examples(self):
        from taxonomy import classify_contribution
        examples = [
            ("Obstacle Detection and Identification Algorithm for Transmission Line Inspection Robot Based on H-CNN",
             "Proposes an object identification algorithm for robotic inspection.", "感知建图与导航"),
            ("Design of Firefighting Robot Guidance System Based on Stereo Vision and Deep Learning",
             "The robot visual guidance method combines stereo images and deep learning.", "感知建图与导航"),
            ("Research on Task Decomposition of Substation Inspection Robot Based on Improved-ISODATA Algorithm",
             "Clustering task decomposition for robot inspection routes.", "感知建图与导航")
        ]
        for title, abstract, expected in examples:
            with self.subTest(title=title):
                self.assertEqual(classify_contribution(title, abstract).category, expected)

    def test_model_json_parser(self):
        from llm_review import parse_model_response
        sample='{"primary_category":"大脑与具身智能","needs_review":false,"reason":"高层任务决策和技能调度"}'
        self.assertEqual(parse_model_response(sample)["primary_category"],"大脑与具身智能")
        self.assertEqual(parse_model_response("Here: `"+"``json\\n"+sample+"\\n```")["primary_category"],"大脑与具身智能")
        with self.assertRaises(ValueError):
            parse_model_response("")

    def test_compact_model_classification(self):
        from llm_review import parse_short_classification
        output="大脑与具身智能|NO|论文研究语言智能体高层任务推理及机器人技能调度"
        result=parse_short_classification(output)
        self.assertEqual(result["primary_category"],"大脑与具身智能")
        self.assertFalse(result["needs_review"])
        self.assertTrue(parse_short_classification(
            "感知建图与导航|YES|论文证据不足但主要围绕场景导航规划"
        )["needs_review"])
        with self.assertRaises(ValueError):
            parse_short_classification("Random text without a category")

    def test_model_multiple_output_forms_and_evidence(self):
        from llm_review import parse_short_classification, validate
        paper_id="paper-test"
        variants=[
            '大脑与具身智能|NO|通过视觉语言模型进行任务分解并调用导航技能',
            '分类：大脑与具身智能\n理由：通过视觉语言模型进行任务分解并调用导航技能',
            '{"category":"大脑与具身智能","needs_review":false,"reason":"通过视觉语言模型进行任务分解并调用导航技能"}',
            'Result: ```json\n{"primary_category":"大脑与具身智能","needs_review":false,"reason":"通过视觉语言模型进行任务分解并调用导航技能"}\n```'
        ]
        for response in variants:
            with self.subTest(response=response[:25]):
                entry=parse_short_classification(response)
                entry["id"]=paper_id
                self.assertIsNotNone(validate(entry,{paper_id}))
        self.assertIsNone(validate({"id":paper_id,"primary_category":"大脑与具身智能",
            "needs_review":"false","reason":"通过视觉语言模型进行任务分解并调用导航技能"},{paper_id}))
        self.assertIsNone(validate({"id":paper_id,"primary_category":"大脑与具身智能",
            "needs_review":False,"reason":"证据不足"},{paper_id}))
        with self.assertRaises(ValueError):
            parse_short_classification("大脑与具身智能 或 感知建图与导航")

    def test_grounding_and_safe_diagnostics(self):
        from llm_review import evidence_supported, safe_diagnostic
        paper={"title":"Vision Language Navigation with Skill Planning",
               "description":"A VLM agent selects navigation skills."}
        self.assertTrue(evidence_supported(paper,"视觉语言技能导航"))
        self.assertFalse(evidence_supported(paper,"触觉传感器实现反射控制"))
        diag=safe_diagnostic("文本|NO|理由",None,None)
        self.assertEqual(diag["shape"],"pipe_like")
        self.assertNotIn("文本",str(diag))

    def test_fresh_review_priority_and_model_override(self):
        from llm_review import prioritize_reviews, apply_model_result
        from main import preserve_model_classification
        from datetime import datetime, timezone
        now=datetime(2026,10,20,tzinfo=timezone.utc)
        old={"id":"old","first_seen":"2026-10-01T12:00:00+00:00","needs_review":True}
        fresh={"id":"new","first_seen":"2026-10-20T01:00:00+00:00","needs_review":True}
        queue, recent, prior=prioritize_reviews([old,fresh],{},now)
        self.assertEqual([r["id"] for r in queue],["new","old"])
        self.assertEqual((recent,prior),(1,1))
        item={"id":"new","title":"VLM robot skill planner",
              "description":"A VLM robot agent uses language instruction to select skills for autonomous navigation. "*3,
              "category":"感知建图与导航","needs_review":True,"tags":["感知建图与导航"]}
        result={"primary_category":"大脑与具身智能","needs_review":False,
                "model_confidence":"HIGH",
                "main_contribution":"视觉语言模型调用技能进行机器人任务规划",
                "reason":"视觉语言模型执行技能调度与高层导航任务规划"}
        event=apply_model_result(item,result,"2026-10-20T02:00:00+00:00")
        self.assertIsNotNone(event)
        refreshed=dict(item,category="感知建图与导航",model_applied=False,needs_review=True)
        refreshed.pop("classification_history",None)
        preserved=preserve_model_classification(refreshed,item)
        self.assertEqual(preserved["category"],"大脑与具身智能")
        changed=dict(item,category="感知建图与导航",model_applied=False,needs_review=True,description="changed")
        self.assertEqual(preserve_model_classification(changed,item)["category"],"感知建图与导航")

    def test_ambiguous_model_category_survives_rule_refresh_without_long_abstract(self):
        from llm_review import apply_model_result, prioritize_reviews
        from main import preserve_model_classification
        from datetime import datetime, timezone
        item={"id":"short","title":"Agentic skill planning","description":"VLM skill planning",
              "category":"感知建图与导航","needs_review":True}
        proposal={"primary_category":"大脑与具身智能","needs_review":True,
                  "reason":"视觉语言模型用于技能规划仍需进一步核查"}
        event=apply_model_result(item,proposal,"2026-10-20T03:00:00+00:00")
        self.assertIsNotNone(event)
        self.assertEqual(item["category"],"感知建图与导航")
        self.assertTrue(item["needs_review"])
        refreshed={"id":"short","title":item["title"],"description":item["description"],
                   "category":"感知建图与导航","needs_review":True}
        outcome=preserve_model_classification(refreshed,item)
        self.assertEqual(outcome["category"],"感知建图与导航")
        self.assertTrue(outcome["needs_review"])
        queue,_,_=prioritize_reviews([outcome],{},datetime(2026,10,20,tzinfo=timezone.utc))
        self.assertEqual(queue,[])
        self.assertEqual(event["status"],"model_pending_review")
        self.assertEqual(item["model_suggested_category"],"大脑与具身智能")

    def test_generalized_special_robot_contribution_boundaries(self):
        from taxonomy import classify_contribution
        cases=[
            ("Adaptive fuzzy PID control for firefighting robot",
             "Robot motion control and tracking experiments.", "小脑与运动控制"),
            ("Visual defect detection algorithm for industrial inspection robot",
             "Robot image recognition and defect detection.", "感知建图与导航"),
            ("Task allocation method based on genetic algorithm for substation inspection robots",
             "Task allocation optimization for a fleet of robots.", "基础软件与系统"),
            ("Adaptive robot climbing with magnetic feet in unknown slippery structure",
             "Locomotion adaptation and climbing control on slippery surfaces.", "小脑与运动控制"),
        ]
        for title,abstract,category in cases:
            with self.subTest(title=title):
                decision=classify_contribution(title,abstract)
                self.assertEqual(decision.category,category)

    def test_individually_reviewed_cases_are_stable(self):
        from main import apply_manual_correction, preserve_model_classification
        records = [
            ("xfjcoder/wam", "小脑与运动控制"),
            ("manankharwar/fusioncore", "感知建图与导航"),
            ("omnilink-tech/omnisim", "基础软件与系统"),
            ("arnavsharmaa/blackbox", "基础软件与系统"),
        ]
        for title, expected in records:
            with self.subTest(title=title):
                paper={"id":title,"title":title,"description":"Robot system",
                       "category":"特种应用与产品","needs_review":True}
                checked=apply_manual_correction(paper)
                self.assertEqual(checked["category"],expected)
                self.assertFalse(checked["needs_review"])
                self.assertTrue(checked["manual_category_override"])
                new_rule=dict(paper,category="特种应用与产品",manual_category_override=False)
                new_rule.pop("classification_history",None)
                restored=preserve_model_classification(new_rule,paper)
                self.assertEqual(restored["category"],expected)

    def test_model_review_manual_corrections_persist(self):
        from main import apply_manual_correction, preserve_model_classification
        cases = [
            ("DR-VLA: Learning Human-Like Quadruped Navigation from Egocentric Web Videos via Domain-Invariant Scene Representations", "感知建图与导航"),
            ("Structure over Reasoning: Unified Zero-Shot Navigation with a Small Vision-Language Model", "感知建图与导航"),
            ("FACT: A Multimodal Force-Action-Track Foundation Model for Human-to-Robot Dexterity", "小脑与运动控制"),
            ("Mapless, Stabilizing, and Anti-Stuck Flipper Control for Articulated Tracked Robots", "小脑与运动控制"),
            ("A Heterogeneous UAV UGV Methodology for Aerial Tracking of Mini Autonomous Cars", "感知建图与导航"),
        ]
        for title, expected in cases:
            with self.subTest(title=title):
                paper = {"id": title, "title": title, "description": "Metadata summary",
                         "category": "大脑与具身智能", "needs_review": True}
                verified = apply_manual_correction(paper)
                self.assertEqual(verified["category"], expected)
                self.assertTrue(verified["manual_category_override"])
                reclassified = {"id": title, "title": title, "description": "Metadata summary",
                                "category": "特种应用与产品", "needs_review": True}
                persisted = preserve_model_classification(reclassified, verified)
                self.assertEqual(persisted["category"], expected)

    def test_model_event_history_deduplicates_retry_but_keeps_revisions(self):
        from llm_review import unique_history
        a={"id":"paper1","status":"model_applied","new_category":"小脑与运动控制","reason":"策略学习方法","changed_at":"first"}
        b=dict(a,changed_at="second")
        c=dict(a,new_category="感知建图与导航",changed_at="third")
        retained=unique_history([a,b,c])
        self.assertEqual(len(retained),2)
        self.assertEqual(retained[0]["changed_at"],"first")

    def test_rule_contribution_corrections_oct_2026(self):
        from taxonomy import classify_contribution
        cases = [
            ("Explosion-proof lithium-ion battery pack – In-depth investigation and experimental study on the design criteria", "硬件与防爆"),
            ("Research on the Pressure Relief Process of Explosion-Proof Pressure Relief Valve for Power Battery Based on Choked Flow", "硬件与防爆"),
            ("Dynamic Inspection Algorithm Based on Substation Inspection Robot", "感知建图与导航"),
            ("Research on Improved Hybrid Polynomial Interpolation Algorithm for Rail Inspection Robot", "小脑与运动控制"),
            ("Hybrid motion planning with dynamics awareness for aerial-ground robots in industrial inspection and maintenance", "感知建图与导航"),
            ("Microcontroller-Based Substation Inspection Robot Design--Software Part", "基础软件与系统"),
            ("Research on Path Optimization Method for Warehouse Inspection Robot", "感知建图与导航"),
            ("AI-Enhanced Radiation Classification in ROS", "感知建图与导航"),
        ]
        for title, expected in cases:
            with self.subTest(title=title):
                self.assertEqual(classify_contribution(title).category, expected)

    def test_contribution_guard_and_relevance(self):
        from contribution_review import contribution_conflict, relevance_status
        self.assertIn("冲突",contribution_conflict(
            {"title":"Quadruped robot gait control with reinforcement learning","description":"locomotion policy"},
            "大脑与具身智能"))
        self.assertEqual(contribution_conflict(
            {"title":"Robot SLAM and odometry","description":"visual localization"},
            "感知建图与导航"),"")
        self.assertEqual(relevance_status("Explosion-proof battery pack design","",False,False,False,[]),
                         "潜在相关（需核实机器人应用）")
        self.assertEqual(relevance_status("Quadruped robot gait control","",True,True,True,["robot"]),
                         "直接相关")

    def test_model_confidence_and_rule_conflict_do_not_override(self):
        from llm_review import apply_model_result
        item={"id":"guard","title":"Quadruped robot gait control with reinforcement learning",
              "description":"A locomotion policy for a quadruped robot",
              "category":"小脑与运动控制","needs_review":True,"rule_confidence":"high"}
        proposal={"primary_category":"大脑与具身智能","needs_review":False,
                  "model_confidence":"HIGH",
                  "main_contribution":"四足机器人步态控制与强化学习",
                  "reason":"四足机器人运动控制研究使用强化学习训练步态策略"}
        result=apply_model_result(item,proposal,"2026-10-20")
        self.assertEqual(item["category"],"小脑与运动控制")
        self.assertTrue(item["needs_review"])
        self.assertFalse(item["model_applied"])
        self.assertEqual(result["status"],"model_pending_review")

    def test_high_confidence_crosscheck_detects_conflict_without_relabeling(self):
        from classification_crosscheck import apply_crosschecks
        sample={"id":"s","title":"Simultaneous Localization and Mapping Methods for Snake-like Robots Based on Gait Adjustment",
                "description":"Snake robot SLAM localization mapping",
                "category":"小脑与运动控制","rule_category":"小脑与运动控制",
                "rule_confidence":"high","needs_review":False}
        apply_crosschecks([sample])
        self.assertEqual(sample["category"],"小脑与运动控制")
        self.assertTrue(sample["needs_review"])
        self.assertEqual(sample["crosscheck_conflicts"][0]["suggested_category"],"感知建图与导航")

    def test_high_confidence_crosscheck_remains_flagged_after_repeated_run(self):
        from classification_crosscheck import apply_crosschecks
        paper={"title":"Simultaneous Localization and Mapping Methods for Snake-like Robots Based on Gait Adjustment",
               "description":"SLAM of snake robots using gait adjustment",
               "category":"小脑与运动控制","rule_category":"小脑与运动控制",
               "rule_confidence":"high","needs_review":False}
        apply_crosschecks([paper])
        first=list(paper["crosscheck_conflicts"])
        self.assertTrue(first)
        apply_crosschecks([paper])
        self.assertEqual(paper["crosscheck_conflicts"],first)
        self.assertTrue(paper["crosscheck_pending"])
        self.assertTrue(paper["needs_review"])

    def test_crosscheck_object_navigation_idempotent(self):
        from classification_crosscheck import apply_crosschecks
        paper={"title":"Can an Embodied Agent Find Your Cat-shaped Mug? LLM-Based Zero-Shot Object Navigation",
               "description":"Language-guided exploration for zero-shot object navigation",
               "category":"大脑与具身智能","rule_category":"大脑与具身智能",
               "rule_confidence":"high","needs_review":False}
        apply_crosschecks([paper])
        self.assertEqual(paper["crosscheck_conflicts"][0]["suggested_category"],"感知建图与导航")
        apply_crosschecks([paper])
        self.assertEqual(len(paper["crosscheck_conflicts"]),1)

    def test_high_confidence_crosscheck_correct_agent_not_flagged(self):
        from classification_crosscheck import apply_crosschecks
        sample={"title":"VLM agent skill orchestration for robot navigation",
                "category":"大脑与具身智能","rule_category":"大脑与具身智能",
                "rule_confidence":"high","needs_review":False}
        apply_crosschecks([sample])
        self.assertFalse(sample["crosscheck_conflicts"])

    def test_priority_retry_four_days_and_manual_handoff(self):
        from llm_review import prioritize_reviews,apply_model_result
        from datetime import datetime,timezone
        now=datetime(2026,10,20,tzinfo=timezone.utc)
        base={"title":"Quadruped robot gait control","description":"Quadruped gait control policy",
              "category":"小脑与运动控制","rule_confidence":"low","needs_review":True}
        p0=dict(base,id="new",first_seen="2026-10-20T01:00:00+00:00")
        p1=dict(base,id="conflict",first_seen="2026-10-01T01:00:00+00:00",crosscheck_pending=True)
        p2=dict(base,id="old",first_seen="2026-10-01T01:00:00+00:00")
        p3=dict(base,id="retry",first_seen="2026-10-01T01:00:00+00:00",
                model_reviewed_uncertain=True,model_review_attempts=1,
                model_reviewed_at="2026-10-15T00:00:00+00:00")
        too_soon=dict(p3,id="too_soon",model_reviewed_at="2026-10-18T00:00:00+00:00")
        exhausted=dict(p3,id="exhausted",model_review_attempts=2)
        candidates,_,_=prioritize_reviews([p3,p2,exhausted,p1,p0,too_soon],{},now)
        self.assertEqual([x["id"] for x in candidates],["new","conflict","old","retry"])
        self.assertTrue(exhausted["manual_review_required"])
        result={"primary_category":"小脑与运动控制","model_confidence":"LOW",
                "needs_review":True,"reason":"四足机器人的步态控制技术仍需验证具体贡献"}
        apply_model_result(p3,result,"2026-10-20T00:00:00+00:00")
        self.assertEqual(p3["model_review_attempts"],2)
        self.assertTrue(p3["manual_review_required"])
        self.assertFalse(p3["model_applied"])

    def test_manual_metadata_review_batch_applied_and_protected(self):
        from main import apply_manual_correction,preserve_model_classification
        cases=[
            ("Simultaneous Localization and Mapping Methods for Snake-like Robots Based on Gait Adjustment","感知建图与导航"),
            ("Can an Embodied Agent Find Your “Cat-shaped Mug”? LLM-Based Zero-Shot Object Navigation","感知建图与导航"),
            ("Benchmark Analysis of Sampling Methods for RRT Path Planning","感知建图与导航"),
            ("Magnetic Field Analytical Calculation of No-Load Electromagnetic Performance of Line-Start Explosion-Proof Permanent Magnet Synchronous Motors Considering Saturation Effect","硬件与防爆"),
            ("Parallel Current-sharing Design of Mine Explosion-proof Lithium-ion Battery Power Supply","硬件与防爆"),
            ("Socially Acceptable Bipedal Robot Navigation via Social Zonotope Network Model Predictive Control","感知建图与导航"),
            ("An improved artemisinin algorithm for task allocation in heterogeneous robot systems for chemical inspection","基础软件与系统"),
            ("Research on inspection task allocation method of inspection robot based on improved genetic algorithm","基础软件与系统"),
            ("Research on Path Optimization Method for Warehouse Inspection Robot","感知建图与导航")
        ]
        for title,expected in cases:
            with self.subTest(title=title):
                item=apply_manual_correction({"title":title,"category":"特种应用与产品",
                                              "needs_review":True,"tags":["特种应用与产品"]})
                self.assertEqual(item["category"],expected)
                self.assertTrue(item["manual_category_override"])
                self.assertFalse(item["needs_review"])
                updated=preserve_model_classification({"title":title,"category":"特种应用与产品",
                                  "tags":["特种应用与产品"],"needs_review":True},item)
                self.assertEqual(updated["category"],expected)

    def test_second_batch_metadata_confirmed_categories(self):
        from main import apply_manual_correction
        cases=[["ROSMonitoring 2.0: Extending ROS Runtime Verification to Services and Ordered Topics","基础软件与系统"],["The Open Stack of Tasks Library: OpenSoT","基础软件与系统"],["Embodied visual route following by an insect-inspired robot","感知建图与导航"],["MiNI-Q: A Miniature, Wire-Free Quadruped with Unbounded, Independently Actuated Leg Joints","硬件与防爆"],["KYON: Semi-Modular Wheel-Legged Quadruped With Agile Bimanual Capability","硬件与防爆"],["Foldable Spherical Pipeline Robot: Design, Control and Simulation","硬件与防爆"],["Design and analysis of pipeline inspection robot based on generalized parallel mechanisms","硬件与防爆"],["Resonant Inductive Coupling Power Transfer for Mid-Sized Inspection Robot","硬件与防爆"],["Research on Inspection Method of Intelligent Factory Inspection Robot for Personnel Safety Protection","感知建图与导航"],["SF6 gas leakage detection method for substation GIS equipment based on intelligent inspection robot technology","感知建图与导航"],["What Makes a Space Traversable? A Formal Definition and On-Policy Certificate for Contact-Rich Egress in Confined Environments","感知建图与导航"],["Design and Implementation of a Semi-Autonomous Quadruped Assistive Robot for Remote Elderly Monitoring and COVID-19 Response","特种应用与产品"]]
        for title,category in cases:
            with self.subTest(title=title):
                item=apply_manual_correction({"title":title,"category":"特种应用与产品",
                                              "needs_review":True,"tags":[]})
                self.assertEqual(item["category"],category)
                self.assertTrue(item["manual_category_override"])
                self.assertFalse(item["needs_review"])

    def test_third_batch_metadata_confirmed_categories(self):
        from main import apply_manual_correction
        cases=[["kevinnana0049-arch/go2w_ROS2","基础软件与系统"],["A Survey of Map Construction and Management Methods for Single Embodied Agents","感知建图与导航"],["From Sky to Soil: A Morphing Aerial-Ground Robot for Seed Deployment","硬件与防爆"],["An Integrated Mobile Robot Framework for Worker Safety, Defect, and Thermal Monitoring in Construction","特种应用与产品"],["Vision-Based Gesture-Controlled Mobile Robot for Human–Robot Interaction Using ROS 2","特种应用与产品"],["What the Elevation Map Cannot See: Semantic-Aware Locomotion and Execution-Aware Navigation for Humanoid Robot","感知建图与导航"],["joey114132/claude-robotics-skills","基础软件与系统"],["Evaluating Long-Horizon Robot Planning under Uncertainty","基础软件与系统"],["AI-Enhanced Radiation Classification in ROS","感知建图与导航"],["BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation","大脑与具身智能"],["SAPS: Shared Autonomy for Policy Steering by Blending Teleoperation with a Pretrained VLA","小脑与运动控制"],["Pose-aware Legged Robot Semantic Exploration with Omnidirectional Perception in Confined Unknown Environments","感知建图与导航"]]
        for title,expected in cases:
            with self.subTest(title=title):
                result=apply_manual_correction({"title":title,"category":"特种应用与产品","needs_review":True,"tags":[]})
                self.assertEqual(result["category"],expected)
                self.assertTrue(result["manual_category_override"])
                self.assertFalse(result["needs_review"])

    def test_independent_model_input_and_rule_evidence_schema(self):
        from contribution_review import contribution_evidence
        category,evidence=contribution_evidence("Robot SLAM and localization","")
        self.assertEqual(category,"感知建图与导航")
        self.assertTrue(evidence)
        from classification_crosscheck import crosscheck_high_confidence
        item={"title":"VLA robot manipulation policy adaptation","category":"大脑与具身智能",
              "rule_category":"大脑与具身智能","rule_confidence":"high","needs_review":False}
        self.assertEqual(crosscheck_high_confidence(item)[0]["suggested_category"],"小脑与运动控制")

    def test_bulk_pending_metadata_decisions(self):
        from main import apply_manual_correction
        cases=[["Design and motion planning of a compact direct-drive leg-wheel robot: DTransleg","硬件与防爆"],["Vision-and-Language Navigation for Human–Robot Collaboration: A Comprehensive Survey","感知建图与导航"],["One-degree-of-freedom planer link leg mechanisms design method for multi objectives through NSGA-II","硬件与防爆"],["Design of Husky V3","硬件与防爆"],["CLASH: Collaborative Large-Small Hierarchical Framework for Continuous Vision-and-Language Navigation","感知建图与导航"],["Development of a Leg-Wheel Quadruped Robot","硬件与防爆"],["Configuration Synthesis and Performance Analysis of 1T2R Decoupled Wheel-Legged Reconfigurable Mechanism","硬件与防爆"],["An Analysis of the Design and Kinematic Characteristics of an Octopedic Land–Air Bionic Robot","硬件与防爆"],["A Compact Reconfigurable Terrestrial-Aerial Robot With Foldable Mechanisms for Rolling, Crawling, and Flying","硬件与防爆"],["Development and Experimental Validation of a Novel Quadruped Robot with a Versatile Robotic Tail","硬件与防爆"],["Inlet duct inspection robot collision-avoidance intrusion trajectory planning","感知建图与导航"],["The control technique and modeling of quadruped robots","小脑与运动控制"],["Humanoid Robot for Firefighting Applications","特种应用与产品"],["Design and implementation of QUADRESCUE: A ROS-based quadruped robot for disaster response support","特种应用与产品"],["A Review of Exploration of the Stable Operation Principle of Quadruped Robots in Complex Terrains","小脑与运动控制"],["Static and Thermal Analysis Using the CFD-FEA Method of the Electronic Enclosure for an EOD Robot","硬件与防爆"],["An unobtrusive RF Sensing Solution For Passive Human-Robot Interaction Verification","感知建图与导航"],["Design and Research of Pharmacy Management Robot Based on Artificial Intelligence","特种应用与产品"]]
        for title,category in cases:
            with self.subTest(title=title):
                item=apply_manual_correction({"title":title,"category":"特种应用与产品","needs_review":True,"tags":[]})
                self.assertEqual(item["category"],category)
                self.assertFalse(item["needs_review"])

    def test_filter_config_reject_score(self):
        item = make_item('Wheel-legged quadruped locomotion', 'https://example.org/w',
                         'arXiv API', '论文（摘要）', 'robot locomotion and motion control')
        self.assertIsNone(rule_enrich(item, {'focus': dict(get_focus(), min_relevance_score=101)}))

    def test_html_industry_filters(self):
        cfg = json.loads(__import__('pathlib').Path('config.json').read_text())
        a = make_item('Firefighting robot navigation', 'https://example.org/ab',
                      'arXiv API', '论文（摘要）', 'Firefighting robot autonomy', utc_now().isoformat())
        html_text = render_html([rule_enrich(a)], [], cfg)
        self.assertIn('全部特种场景', html_text)
        self.assertIn('特种场景直接相关', html_text)
        self.assertIn('消防与应急救援', html_text)

if __name__ == '__main__':
    unittest.main()
