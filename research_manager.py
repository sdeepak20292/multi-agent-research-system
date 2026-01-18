from agents import Runner, trace, gen_trace_id
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent
from critic_agent import critic_agent, CriticFeedback
import asyncio


class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Initial report written..."

            yield "Reviewing report for gaps..."
            feedback = await self.review_report(report)

            if feedback.suggested_searches:
                yield "Performing follow-up research..."
                followup_results = await self.perform_followup_searches(feedback)

                yield "Rewriting improved report..."
                report = await self.write_report(
                    query,
                    search_results + followup_results,
                )
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
            email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report

    async def review_report(self, report: ReportData) -> CriticFeedback:
        print("Reviewing report with critic agent...")
        result = await Runner.run(
            critic_agent,
            report.markdown_report,
        )
        print("Critic review complete")
        return result.final_output_as(CriticFeedback)


    async def perform_followup_searches(
        self, feedback: CriticFeedback
    ) -> list[str]:
        print("Performing follow-up searches...")
        tasks = []

        for query in feedback.suggested_searches:
            item = WebSearchItem(
                query=query,
                reason="Suggested by critic to improve report quality",
            )
            tasks.append(asyncio.create_task(self.search(item)))

        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)

        print("Follow-up searches complete")
        return results


        # The above code defines a ResearchManager class that helps orchestrate the workflow for a "deep research" application.
        #
        # Key components explained:
        #
        # - perform_searches: Given a search plan (a list of search items), it kicks off asynchronous search tasks for each item,
        #   collects their results as they complete, and provides progress updates.
        #
        # - search: Performs a single search for a query and reason, running the search_agent asynchronously. If successful,
        #   it returns the output; otherwise, returns None on error.
        #
        # - write_report: Given an original query and the aggregated search results, it invokes the writer_agent to produce
        #   a final, detailed report (as markdown and summary).
        #
        # - send_email: Given a ReportData object (containing the markdown report), it runs the email_agent to send
        #   the report via email. It returns the report object after sending.
        #
        # Each key step (search, report writing, emailing) is asynchronous, utilizes agent-based tasks, and emits basic console logging.
        # The design enables automated research: planning searches, fetching results, synthesizing a markdown report, and then emailing it.