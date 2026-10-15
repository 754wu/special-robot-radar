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
