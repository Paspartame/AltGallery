import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CatalogTests(unittest.TestCase):
    def test_only_three_expected_apps_and_fork_urls(self):
        data = json.loads((ROOT / "all-apps.json").read_text())
        self.assertEqual({a["name"] for a in data["apps"]}, {"Roam Control", "Lyricify Mobile", "Swipt Nightly"})
        self.assertEqual(len(data["apps"]), 3)
        for app in data["apps"]:
            self.assertIn("raw.githubusercontent.com/Paspartame/AltGallery/master/", app["iconURL"])
            for ver in app["versions"]:
                self.assertNotIn("bebound/AltGallery", ver["downloadURL"])
                self.assertIn("github.com/", ver["downloadURL"])

    def test_roam_identity_and_minimum_release(self):
        roam = next(a for a in json.loads((ROOT / "all-apps.json").read_text())["apps"] if a["name"] == "Roam Control")
        self.assertEqual(roam["bundleIdentifier"], "com.roamcontrol")
        self.assertGreaterEqual(tuple(map(int, roam["versions"][0]["version"].lstrip("v").split("."))), (0, 9, 9))

    def test_mobile_tag_pattern_is_strict(self):
        pattern = re.compile(r"^mobile-v(\d+\.\d+\.\d+)$")
        self.assertIsNotNone(pattern.fullmatch("mobile-v1.6.0"))
        for bad in ("v1.6.0", "mobile-v1.6", "mobile-v1.6.0-extra", "nightly"):
            self.assertIsNone(pattern.fullmatch(bad))

if __name__ == "__main__":
    unittest.main()
