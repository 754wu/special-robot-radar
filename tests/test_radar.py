import unittest
from main import make_item, normalize_link, rule_enrich, esc

class RadarTests(unittest.TestCase):
    def test_normalize_url(self):
        self.assertEqual(normalize_link('https://example.org/a/#f'), 'https://example.org/a')

    def test_classify_brain(self):
        item = make_item('Agentic VLN navigation', 'https://example.org/a', 'arXiv', '论文（摘要）',
                         'vision-language models call skills for robot navigation')
        classified = rule_enrich(item)
        self.assertIsNotNone(classified)
        self.assertIn('大脑与具身智能', classified['tags'])

    def test_html_escape(self):
        self.assertEqual(esc('<script>'), '&lt;script&gt;')

if __name__ == '__main__':
    unittest.main()
