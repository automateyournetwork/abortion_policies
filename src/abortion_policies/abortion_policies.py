import sys
import os
import time
import json
import requests
import rich_click as click
import yaml
import cairosvg
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from gtts import gTTS
from rich.console import Console
from rich.table import Table

class AbortionPolicies():
    def __init__(self,
                token):
        self.token = token

    def abortion_policies(self):
        parsed_json = json.dumps(self.gestational_limits(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.insurance_coverage(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.minors(), indent=4, sort_keys=True)
        self.all_files(parsed_json)
        parsed_json = json.dumps(self.waiting_period(), indent=4, sort_keys=True)
        self.all_files(parsed_json)

    def gestational_limits(self):
        payload={}
        headers = {
        'token': self.token
        }
        self.url = "https://api.abortionpolicyapi.com/v1/gestational_limits/states/"
        response = requests.request("GET", self.url, headers=headers, data=payload)
        all_json = response.json()
        parsed_json = all_json
        return(parsed_json)

    def insurance_coverage(self):
        payload={}
        headers = {
        'token': self.token
        }
        self.url = "https://api.abortionpolicyapi.com/v1/insurance_coverage/states/"
        response = requests.request("GET", self.url, headers=headers, data=payload)
        all_json = response.json()
        parsed_json = all_json
        return(parsed_json)

    def minors(self):
        payload={}
        headers = {
        'token': self.token
        }
        self.url = "https://api.abortionpolicyapi.com/v1/minors/states/"
        response = requests.request("GET", self.url, headers=headers, data=payload)
        all_json = response.json()
        parsed_json = all_json
        return(parsed_json)

    def waiting_period(self):
        payload={}
        headers = {
        'token': self.token
        }
        self.url = "https://api.abortionpolicyapi.com/v1/waiting_periods/states/"
        response = requests.request("GET", self.url, headers=headers, data=payload)
        all_json = response.json()
        parsed_json = all_json
        return(parsed_json)

    def json_file(self, parsed_json):
        if "gestational" in self.url:
            with open('Gestational Limits/JSON/Gestational Limits.json', 'w' ) as f:
                f.write(parsed_json)

        if "insurance" in self.url:
            with open('Insurance Coverage/JSON/Insurance Coverage.json', 'w' ) as f:
                f.write(parsed_json)

        if "minors" in self.url:
            with open('Minors/JSON/Minors.json', 'w' ) as f:
                f.write(parsed_json)

        if "waiting_period" in self.url:
            with open('Waiting Period/JSON/Waiting Period.json', 'w' ) as f:
                f.write(parsed_json)

    def yaml_file(self, parsed_json):
        clean_yaml = yaml.dump(json.loads(parsed_json), default_flow_style=False)
        if "gestational" in self.url:
            with open('Gestational Limits/YAML/Gestational Limits.yaml', 'w' ) as f:
                f.write(clean_yaml)        

        if "insurance" in self.url:
            with open('Insurance Coverage/YAML/Insurance Coverage.yaml', 'w' ) as f:
                f.write(parsed_json)

        if "minors" in self.url:
            with open('Minors/YAML/Minors.yaml', 'w' ) as f:
                f.write(parsed_json)

        if "waiting_period" in self.url:
            with open('Waiting Period/YAML/Waiting Period.yaml', 'w' ) as f:
                f.write(parsed_json)

    def text_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        text_template = env.get_template('abortion_policies_text.j2')
        if "gestational" in self.url:
            for state,policy in json.loads(parsed_json).items():
                text_output = text_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                with open(f'Gestational Limits/Text/{ state } Gestational Limits.txt', 'w' ) as f:
                    f.write(text_output)

        if "insurance" in self.url:
            for state,policy in json.loads(parsed_json).items():
                text_output = text_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                with open(f'Insurance Coverage/Text/{ state } Insurance Coverage.txt', 'w' ) as f:
                    f.write(text_output)

        if "minors" in self.url:
            for state,policy in json.loads(parsed_json).items():
                text_output = text_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                with open(f'Minors/Text/{ state } Minors.txt', 'w' ) as f:
                    f.write(text_output)

        if "waiting_period" in self.url:
            for state,policy in json.loads(parsed_json).items():
                text_output = text_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                with open(f'Waiting Period/Text/{ state } Waiting Period.txt', 'w' ) as f:
                    f.write(text_output)

    def csv_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        csv_template = env.get_template('abortion_policies_csv.j2')      
        csv_output = csv_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json))
        if "gestational" in self.url:                                         
            with open('Gestational Limits/Spreadsheet/Gestational Limits.csv', 'w' ) as f:
                f.write(csv_output)

        if "insurance" in self.url:                                         
            with open('Insurance Coverage/Spreadsheet/Insurance Coverage.csv', 'w' ) as f:
                f.write(csv_output)

        if "minors" in self.url:                                         
            with open('Minors/Spreadsheet/Minors.csv', 'w' ) as f:
                f.write(csv_output)

        if "waiting_period" in self.url:                                         
            with open('Waiting Period/Spreadsheet/Waiting Period.csv', 'w' ) as f:
                f.write(csv_output)

    def markdown_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        markdown_template = env.get_template('abortion_policies_markdown.j2')      
        markdown_output = markdown_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json))
        if "gestational" in self.url:                                         
            with open('Gestational Limits/Markdown/Gestational Limits.md', 'w' ) as f:
                f.write(markdown_output)

        if "insurance" in self.url:                                         
            with open('Insurance Coverage/Markdown/Insurance Coverage.md', 'w' ) as f:
                f.write(markdown_output)

        if "minors" in self.url:
            with open('Minors/Markdown/Minors.md', 'w' ) as f:
                f.write(markdown_output)

        if "waiting_period" in self.url:
            with open('Waiting Period/Markdown/Waiting Period.md', 'w' ) as f:
                f.write(markdown_output)

    def html_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        html_template = env.get_template('abortion_policies_html.j2')      
        html_output = html_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json))
        if "gestational" in self.url:                                         
            with open('Gestational Limits/HTML/Gestational Limits.html', 'w' ) as f:
                f.write(html_output)

        if "insurance" in self.url:                                         
            with open('Insurance Coverage/HTML/Insurance Coverage.html', 'w' ) as f:
                f.write(html_output)

        if "minors" in self.url:                                         
            with open('Minors/HTML/Minors.html', 'w' ) as f:
                f.write(html_output)

        if "waiting_period" in self.url:                                         
            with open('Waiting Period/HTML/Waiting Period.html', 'w' ) as f:
                f.write(html_output)

    def mindmap_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mindmap_template = env.get_template('abortion_policies_mindmap.j2')      
        mindmap_output = mindmap_template.render(api = self.url,
                                         data_to_template = json.loads(parsed_json))
        if "gestational" in self.url:                                         
            with open('Gestational Limits/Mindmap/Gestational Limits.md', 'w' ) as f:
                f.write(mindmap_output)

        if "insurance" in self.url:
            with open('Insurance Coverage/Mindmap/Insurance Coverage.md', 'w' ) as f:
                f.write(mindmap_output)

        if "minors" in self.url:
            with open('Minors/Mindmap/Minors.md', 'w' ) as f:
                f.write(mindmap_output)

        if "waiting_period" in self.url:
            with open('Waiting Period/Mindmap/Waiting Period.md', 'w' ) as f:
                f.write(mindmap_output)

    def mp3_file(self, parsed_json):
        template_dir = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(str(template_dir)))
        mp3_template = env.get_template('abortion_policies_mp3.j2')
        language = "en-US"
        if "gestational" in self.url:
            for state,policy in json.loads(parsed_json).items():
                mp3_output = mp3_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                mp3 = gTTS(text = mp3_output, lang=language)
                # Save MP3
                mp3.save(f'Gestational Limits/MP3/{ state } Gestational Limits.mp3')
                time.sleep(30)

        if "insurance" in self.url:
            for state,policy in json.loads(parsed_json).items():
                mp3_output = mp3_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                mp3 = gTTS(text = mp3_output, lang=language)
                # Save MP3
                mp3.save(f'Insurance Coverage/MP3/{ state } Insurance Coverage.mp3')
                time.sleep(30)

        if "minors" in self.url:
            for state,policy in json.loads(parsed_json).items():
                mp3_output = mp3_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                mp3 = gTTS(text = mp3_output, lang=language)
                # Save MP3
                mp3.save(f'Minors/MP3/{ state } Minors.mp3')
                time.sleep(30)

        if "waiting" in self.url:
            for state,policy in json.loads(parsed_json).items():
                mp3_output = mp3_template.render(api = self.url,
                                                state = state,
                                                policy = policy)
                mp3 = gTTS(text = mp3_output, lang=language)
                # Save MP3
                mp3.save(f'Waiting Period/MP3/{ state } Waiting Period.mp3')
                time.sleep(30)

    def svg_file(self, parsed_json):
        console = Console(record=True)
        if "gestational" in self.url:
            table = Table(title=f"Gestational Limits")
            table.add_column("State", style="bold blue", justify="center")
            table.add_column("Banned After Weeks Since Last Menstrual Period", style="bold green", justify="center")
            table.add_column("Life Exception", style="bold green", justify="center")
            table.add_column("Health Exception", style="bold green", justify="center")
            table.add_column("Fetal Health Exception", style="bold green", justify="center")
            table.add_column("Rape or Incest Exception", style="bold green", justify="center")
            table.add_column("Last Updated", style="bold green", justify="center")
            for state,policy in json.loads(parsed_json).items():
                if 'banned_after_weeks_since_LMP' in policy:
                    banned_after_weeks_since_LMP = policy['banned_after_weeks_since_LMP']
                else:
                    banned_after_weeks_since_LMP = "No"
                if 'exception_life' in policy:
                    exception_life = policy['exception_life']
                else:
                    exception_life = "No"
                if 'exception_health' in policy:
                    exception_health = policy['exception_health']
                else:
                    exception_health = "N/A"
                if 'exception_fetal' in policy:
                    exception_fetal = policy['exception_fetal']
                else:
                    exception_fetal = "N/A"
                if 'exception_rape_or_incest' in policy:
                    exception_rape_or_incest = policy['exception_rape_or_incest']
                else:
                    exception_rape_or_incest = "N/A"
                if 'Last Updated' in policy:
                    last_updated = policy['Last Updated']
                else:
                    last_updated = "N/A"                    
                table.add_row(f"{ state }",str(banned_after_weeks_since_LMP),str(exception_life),str(exception_health),str(exception_fetal),str(exception_rape_or_incest),str(last_updated))
            console.print(table, justify="center")
            console.save_svg("Gestational Limits/SVG/Gestational Limits.svg",
                             title="Gestational Limits")

        if "insurance" in self.url:
            table = Table(title=f"Insurance Coverage")
            table.add_column("State", style="bold blue", justify="center")
            table.add_column("Requires Coverage", style="bold green", justify="center")
            table.add_column("Private Coverage No Restrictions", style="bold green", justify="center")
            table.add_column("Private Coverage Exception Life", style="bold green", justify="center")
            table.add_column("Private Coverage Exception Health", style="bold green", justify="center")
            table.add_column("Private Coverage Exception Fetal", style="bold green", justify="center")
            table.add_column("Private Coverage Exception Rape or Incest", style="bold green", justify="center")
            table.add_column("Exchange Coverage No Restrictions", style="bold green", justify="center")
            table.add_column("Exchange Coverage Exception Life", style="bold green", justify="center")
            table.add_column("Exchange Coverage Exception Health", style="bold green", justify="center")
            table.add_column("Exchange Coverage Exception Fetal", style="bold green", justify="center")
            table.add_column("Exchange Coverage Exception Rape or Incest", style="bold green", justify="center")
            table.add_column("Exchange Coverage Forbids Coverage", style="bold green", justify="center")
            table.add_column("Medicaid Coverage Provider Patient Decision", style="bold green", justify="center")
            table.add_column("Medicaid Coverage Exception Life", style="bold green", justify="center")
            table.add_column("Medicaid Coverage Exception Health", style="bold green", justify="center")
            table.add_column("Medicaid Coverage Exception Fetal", style="bold green", justify="center")
            table.add_column("Medicaid Coverage Exception Rape or Incest", style="bold green", justify="center")
            table.add_column("Last Updated", style="bold green", justify="center")
            for state,policy in json.loads(parsed_json).items():
                if 'requires_coverage' in policy:
                    requires_coverage = policy['requires_coverage']
                else:
                    requires_coverage = "No"
                if 'private_coverage_no_restrictions' in policy:
                    private_coverage_no_restrictions = policy['private_coverage_no_restrictions']
                else:
                    private_coverage_no_restrictions = "N/A"
                if 'private_exception_life' in policy:
                    private_exception_life = policy['private_exception_life']
                else:
                    private_exception_life = "N/A"
                if 'private_exception_health' in policy:
                    private_exception_health = policy['private_exception_health']
                else:
                    private_exception_health = "N/A"
                if 'private_exception_fetal' in policy:
                    private_exception_fetal = policy['private_exception_fetal']
                else:
                    private_exception_fetal = "N/A"
                if 'private_exception_rape_or_incest' in policy:
                    private_exception_rape_or_incest = policy['private_exception_rape_or_incest']
                else:
                    private_exception_rape_or_incest = "N/A"
                if 'exchange_coverage_no_restrictions' in policy:
                    exchange_coverage_no_restrictions = policy['exchange_coverage_no_restrictions']
                else:
                    exchange_coverage_no_restrictions = "N/A"
                if 'exchange_exception_life' in policy:
                    exchange_exception_life = policy['exchange_exception_life']
                else:
                    exchange_exception_life = "N/A"
                if 'exchange_exception_health' in policy:
                    exchange_exception_health = policy['exchange_exception_health']
                else:
                    exchange_exception_health = "N/A"
                if 'exchange_exception_fetal' in policy:
                    exchange_exception_fetal = policy['exchange_exception_fetal']
                else:
                    exchange_exception_fetal = "N/A"
                if 'exchange_exception_rape_or_incest' in policy:
                    exchange_exception_rape_or_incest = policy['exchange_exception_rape_or_incest']
                else:
                    exchange_exception_rape_or_incest = "N/A"
                if 'exchange_forbids_coverage' in policy:
                    exchange_forbids_coverage = policy['exchange_forbids_coverage']
                else:
                    exchange_forbids_coverage = "N/A"
                if 'medicaid_coverage_provider_patient_decision' in policy:
                    medicaid_coverage_provider_patient_decision = policy['medicaid_coverage_provider_patient_decision']
                else:
                    medicaid_coverage_provider_patient_decision = "N/A"
                if 'medicaid_exception_life' in policy:
                    medicaid_exception_life = policy['medicaid_exception_life']
                else:
                    medicaid_exception_life = "N/A"
                if 'medicaid_exception_health' in policy:
                    medicaid_exception_health = policy['medicaid_exception_health']
                else:
                    medicaid_exception_health = "N/A"
                if 'medicaid_exception_fetal' in policy:
                    medicaid_exception_fetal = policy['medicaid_exception_fetal']
                else:
                    medicaid_exception_fetal = "N/A"
                if 'medicaid_exception_rape_or_incest' in policy:
                    medicaid_exception_rape_or_incest = policy['medicaid_exception_rape_or_incest']
                else:
                    medicaid_exception_rape_or_incest = "N/A"                    
                if 'Last Updated' in policy:
                    last_updated = policy['Last Updated']
                else:
                    last_updated = "N/A"                    
                table.add_row(f"{ state }",str(requires_coverage),str(private_coverage_no_restrictions),str(private_exception_life),str(private_exception_health),str(private_exception_fetal),str(private_exception_rape_or_incest),str(exchange_coverage_no_restrictions),str(exchange_exception_life),str(exchange_exception_health),str(exchange_exception_fetal),str(exchange_exception_rape_or_incest),str(exchange_forbids_coverage),str(medicaid_coverage_provider_patient_decision),str(medicaid_exception_life),str(medicaid_exception_health),str(medicaid_exception_fetal),str(medicaid_exception_rape_or_incest),str(last_updated))
            console.print(table, justify="center")
            console.save_svg("Insurance Coverage/SVG/Insurance Coverage.svg",
                             title="Insurance Coverage")

        if "minors" in self.url:
            table = Table(title=f"Minors")
            table.add_column("State", style="bold blue", justify="center")
            table.add_column("Below Age", style="bold green", justify="center")
            table.add_column("Parental Consent Required", style="bold green", justify="center")
            table.add_column("Parental Notification Required", style="bold green", justify="center")
            table.add_column("Parents Required", style="bold green", justify="center")
            table.add_column("Judicial Bypass Available", style="bold green", justify="center")
            table.add_column("Allows Minor to Consent", style="bold green", justify="center")
            table.add_column("Last Updated", style="bold green", justify="center")
            for state,policy in json.loads(parsed_json).items():
                if 'below_age' in policy:
                    below_age = policy['below_age']
                else:
                    below_age = "No"
                if 'parental_consent_required' in policy:
                    parental_consent_required = policy['parental_consent_required']
                else:
                    parental_consent_required = "N/A"
                if 'parental_notification_required' in policy:
                    parental_notification_required = policy['parental_notification_required']
                else:
                    parental_notification_required = "N/A"
                if 'parents_required' in policy:
                    parents_required = policy['parents_required']
                else:
                    parents_required = "N/A"
                if 'judicial_bypass_available' in policy:
                    judicial_bypass_available = policy['judicial_bypass_available']
                else:
                    judicial_bypass_available = "N/A"
                if 'allows_minor_to_consent' in policy:
                    allows_minor_to_consent = policy['allows_minor_to_consent']
                else:
                    allows_minor_to_consent = "N/A"
                if 'Last Updated' in policy:
                    last_updated = policy['Last Updated']
                else:
                    last_updated = "N/A"                    
                table.add_row(f"{ state }",str(below_age),str(parental_consent_required),str(parental_notification_required),str(parents_required),str(judicial_bypass_available),str(allows_minor_to_consent),str(last_updated))
            console.print(table, justify="center")
            console.save_svg("Minors/SVG/Minors.svg",
                             title="Minors")

        if "waiting_period" in self.url:
            table = Table(title=f"Waiting Period")
            table.add_column("State", style="bold blue", justify="center")
            table.add_column("Waiting Period Hours", style="bold green", justify="center")
            table.add_column("Counseling Visits", style="bold green", justify="center")
            table.add_column("Exception Health", style="bold green", justify="center")
            table.add_column("Waiting Period Notes", style="bold green", justify="center")
            table.add_column("Last Updated", style="bold green", justify="center")
            for state,policy in json.loads(parsed_json).items():
                if 'waiting_period_hours' in policy:
                    waiting_period_hours = policy['waiting_period_hours']
                else:
                    waiting_period_hours = "No"
                if 'counseling_visits' in policy:
                    counseling_visits = policy['counseling_visits']
                else:
                    counseling_visits = "N/A"
                if 'exception_health' in policy:
                    exception_health = policy['exception_health']
                else:
                    exception_health = "N/A"
                if 'waiting_period_notes' in policy:
                    waiting_period_notes = policy['waiting_period_notes']
                else:
                    waiting_period_notes = "N/A"
                if 'Last Updated' in policy:
                    last_updated = policy['Last Updated']
                else:
                    last_updated = "N/A"                    
                table.add_row(f"{ state }",str(waiting_period_hours),str(counseling_visits),str(exception_health),str(waiting_period_notes),str(last_updated))
            console.print(table, justify="center")
            console.save_svg("Waiting Period/SVG/Waiting Period.svg",
                             title="Waiting Period")

    def png_file(self, parsed_json):
        self.svg_file(parsed_json)
        if "gestational" in self.url:
            cairosvg.svg2png(
                url="Gestational Limits/SVG/Gestational Limits.svg", write_to="Gestational Limits/PNG/Gestational Limits.png")

        if "insurance" in self.url:
            cairosvg.svg2png(
                url="Insurance Coverage/SVG/Insurance Coverage.svg", write_to="Insurance Coverage/PNG/Insurance Coverage.png")

        if "minors" in self.url:
            cairosvg.svg2png(
                url="Minors/SVG/Minors.svg", write_to="Minors/PNG/Minors.png")

        if "waiting_period" in self.url:
            cairosvg.svg2png(
                url="Waiting Period/SVG/Waiting Period.svg", write_to="Waiting Period/PNG/Waiting Period.png")

    def all_files(self, parsed_json):
        self.json_file(parsed_json)
        self.yaml_file(parsed_json)
        self.text_file(parsed_json)
        self.csv_file(parsed_json)
        self.markdown_file(parsed_json)
        self.html_file(parsed_json)
        self.mindmap_file(parsed_json)
        self.svg_file(parsed_json)
        self.png_file(parsed_json)
        self.mp3_file(parsed_json)
        
@click.command()
@click.option('--token',
    prompt="Abortion API Token",
    help="The Abortion API Token",
    required=True, hide_input=True,envvar="TOKEN")
def cli(token):
    invoke_class = AbortionPolicies(token)
    invoke_class.abortion_policies()

if __name__ == "__main__":
    cli()
