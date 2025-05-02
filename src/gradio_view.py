import gradio as gr
from subscription_manager import SubscriptionManager
from github_client import GitHubClient
from report_generator import ReportGenerator
from llm import LLM
from config import Config
from logger import LOG

cfg = Config()
subscript_manager = SubscriptionManager(cfg.subscriptions_file)
github_client = GitHubClient(cfg.github_token)
llm = LLM(cfg)
report_generate = ReportGenerator(llm,cfg.report_types)

def generate_report_by_date_range(repo,days):
    LOG.info(f"begin invoke action....,days:{days}")
    progress_file = github_client.github_client.export_progress_by_date_range(repo=repo,days=days)
    report,report_file = report_generate.generate_github_report(progress_file)
    return report,report_file

gradio_server = gr.Interface(
    fn = generate_report_by_date_range,
    inputs=[
        gr.Dropdown(subscript_manager.get_subscriptions(),label="订阅项目",info="已经订阅的项目"),
        gr.Slider(value=2,minimum=1,maximum=7,step=1,label="项目周期",info="生成项目过去一段时间进展，单位：天")
    ],
    outputs=[
        gr.Markdown(),
        gr.File(label="下载报告")
    ]
)

if __name__ == "__main__":
    gradio_server.launch(share=False)
    # gradio_server.launch(share=True,server_name="0.0.0.0",auth=("admin","123456"))

