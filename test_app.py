import unittest

import app


class CardBankTests(unittest.TestCase):
    def setUp(self):
        self.client = app.app.test_client()

    def test_school_logo_is_served_as_png(self):
        response = self.client.get("/school-logo.png")
        self.assertEqual(response.status_code, 200)
        self.assertIn("image/png", response.content_type)
        self.assertTrue(response.data.startswith(b"\x89PNG\r\n\x1a\n"))
        response.close()

    def test_home_and_bank_endpoint(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn("المدرسة الوطنية لمهندسي المدينة".encode(), page.get_data())
        page.close()

        response = self.client.get("/api/banks")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data["general"]["questions"]), 20)
        self.assertEqual(len(data["cyber"]["questions"]), 20)
        self.assertEqual(len(data["day1"]["questions"]), 60)
        self.assertEqual(
            data["day1"]["title"],
            "كسر الجليد – اليوم الأول | الأمن السيبراني لغير التقنيين في عصر الذكاء الاصطناعي",
        )

    def test_question_numbers_types_and_answers(self):
        data = self.client.get("/api/banks").get_json()
        supported = {"open_ended", "team_challenge", "this_or_that", "single_choice"}

        for bank_name in ("general", "cyber"):
            questions = data[bank_name]["questions"]
            self.assertEqual([q["number"] for q in questions], list(range(1, 21)))
            self.assertTrue({q["type"] for q in questions}.issubset(supported))

        questions = data["day1"]["questions"]
        self.assertEqual([q["number"] for q in questions], list(range(1, 61)))
        self.assertEqual(len({q["id"] for q in questions}), 60)
        for question in questions:
            self.assertIn(question["type"], supported)
            if question["type"] in {"single_choice", "this_or_that"}:
                self.assertGreaterEqual(len(question["options"]), 2)
            if question["type"] == "single_choice":
                option_ids = {option["id"] for option in question["options"]}
                self.assertIn(question["correctOptionId"], option_ids)
                self.assertTrue(question.get("explanation"))


if __name__ == "__main__":
    unittest.main()
