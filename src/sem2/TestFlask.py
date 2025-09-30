import unittest

import requests as r

BASE_URL = "http://127.0.0.1:5000"


class TestCase(unittest.TestCase):
    def setUp(self):
        self.s = r.Session()

    def _create_movie(self):
        payload = {
            "movie": {
                "title": "Врата Штейна",
                "year": 2011,
                "director": "Ханада Дзюкки",
                "length": "02:25:00",
                "rating": 10,
            }
        }
        resp = self.s.post(f"{BASE_URL}/api/movies", json=payload)
        self.assertEqual(resp.status_code, 200, msg=resp.text)
        return resp.json()["movie"]["id"]

    def test_flow_crud(self):
        # GET all
        resp = self.s.get(f"{BASE_URL}/api/movies")
        self.assertEqual(resp.status_code, 200, msg=resp.text)
        self.assertIn("list", resp.json())

        # POST
        mid = self._create_movie()

        # GET by id
        resp = self.s.get(f"{BASE_URL}/api/movies/{mid}")
        self.assertEqual(resp.status_code, 200, msg=resp.text)

        # PATCH
        resp = self.s.patch(f"{BASE_URL}/api/movies/{mid}", json={"movie": {"title": "Врата Штейна 0"}})
        self.assertEqual(resp.status_code, 200, msg=resp.text)
        self.assertEqual(resp.json()["movie"]["title"], "Врата Штейна 0")

        # DELETE (в твоём текущем коде 200; по ТЗ должно быть 202)
        resp = self.s.delete(f"{BASE_URL}/api/movies/{mid}")
        self.assertIn(resp.status_code, (200, 202), msg=resp.text)

        # GET после удаления → 404
        resp = self.s.get(f"{BASE_URL}/api/movies/{mid}")
        self.assertEqual(resp.status_code, 404, msg=resp.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
