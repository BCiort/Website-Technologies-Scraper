import json
import re
from typing import Dict, List, Any
class Analyzer:
    def __init__(self, rules_path: str = "data/rules.json"):
        with open(rules_path, 'r', encoding="utf-8") as f:
            self.technologies = json.load(f)

    def analyze(self, domain_data: Dict[str, Any]) -> List[Dict[str, str]]:
        found_techs = []
        html_content = domain_data.get("html", "")
        headers = domain_data.get("headers", {})

        if domain_data.get("error") or not html_content:
            return found_techs

        for tech in self.technologies:
            tech_name = tech["name"]
            rules = tech.get("rules", {})
            matched = False

            if "headers" in rules and not matched:
                for header_key, regex_pattern in rules["headers"].items():
                    actual_header_value = next((v for k, v in headers.items() if k.lower() == header_key.lower()), None)

                    if actual_header_value and re.search(regex_pattern, actual_header_value, re.IGNORECASE):
                        found_techs.append({
                            "name": tech_name,
                            "category": tech["category"]
                        })
                        matched = True
                        break

            if "html" in rules and not matched:
                for regex_pattern in rules["html"]:
                    if re.search(regex_pattern, html_content, re.IGNORECASE):
                        found_techs.append({
                            "name": tech_name,
                            "category": tech["category"]
                        })
                        matched = True
                        break

            return found_techs
