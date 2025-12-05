from src.validator import AutoValidator
from src.export_bugcrowd import BugcrowdExporter
from src.discord_reporter import DiscordReporter

def run_bugcrowd_export_cycle(webhook):
    print("🚀 Quantum Infinity v∞.6 Cycle Starting...")
    validator = AutoValidator()
    validated_path = validator.run()

    exporter = BugcrowdExporter(validated_path)
    export_path = exporter.export_all()

    reporter = DiscordReporter(webhook)
    with open(export_path, "r") as f:
        data = json.load(f)
    reporter.send_embed(export_path, data)

    print("✅ Quantum Infinity v∞.6 — Auto Validation and Bugcrowd Export Completed Successfully.")
