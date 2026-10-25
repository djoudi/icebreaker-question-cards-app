import unittest

import app


class CardBankTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_institute_logo_is_served_as_svg(self):
        response = self.client.get("/institute-logo.svg")
        self.assertEqual(response.status_code, 200)
        self.assertIn("image/svg+xml", response.content_type)
        self.assertIn(b"<svg", response.data[:500])
        response.close()

    def test_home_and_bank_endpoint(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("اختر بطاقة".encode(), page.get_data())
        page.close()
        response = self.client.get("/api/banks")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["general"]["questions"]), 20)
        self.assertEqual(len(data["cyber"]["questions"]), 20)

    def test_question_numbers_and_types(self):
        data = self.client.get("/api/banks").get_json()
        supported = {"open_ended", "team_challenge", "this_or_that", "single_choice"}
        for bank in data.values():
            questions = bank["questions"]
            self.assertEqual([q["number"] for q in questions], list(range(1, 21)))
            self.assertTrue({q["type"] for q in questions}.issubset(supported))


if __name__ == "__main__":
    unittest.main()
