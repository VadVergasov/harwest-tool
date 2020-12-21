import os

from datetime import datetime
from harwest.lib.utils import config


class Submissions:
  def __init__(self, submissions_directory):
    self.readme_path = os.path.join(submissions_directory, "README.md")
    self.submission_json_path = \
      os.path.join(submissions_directory, "submissions.json")
    self.store = config.load_submissions_data(self.submission_json_path)

  def add(self, submission,platform="codeforces"):
    submission_id = submission['submission_id']
    self.store[str(submission_id)] = submission
    self.__generate_readme(list(self.store.values()),platform)
    config.write_submissions_data(self.submission_json_path, self.store)

  def contains(self, submission_id):
    return str(submission_id) in self.store

  def __generate_readme(self, submissions,platform):
    submissions = sorted(
      submissions,
      key=lambda s: datetime.strptime(s['timestamp'], '%b/%d/%Y %H:%M'),
      reverse=True
    )
    index = len(set([x['problem_url'] for x in submissions]))
    problems = set()
    rows = []
    for submission in submissions:
      if submission['problem_url'] in problems:
        continue
      problems.add(submission['problem_url'])
      row = str(index) + " | "
      if platform == 'atcoder':
        row += '[{problem_name}]({problem_url}) | '.format(
          problem_name=submission['problem_name'],
          problem_url=submission['problem_url']
        )
      else:
        row += '[{problem_index} - {problem_name}]({problem_url}) | '.format(
          problem_index=submission['problem_index'],
          problem_name=submission['problem_name'],
          problem_url=submission['problem_url']
        )
      row += '[{lang}](./{path}) | '.format(
        lang=submission['language'],
        path=submission['path'].replace('\\', '/')
      )
      row += ' '.join(['`{tag}`'.format(tag=x) for x in submission['tags']])
      row += " | "
      row += str(submission['timestamp']) + " | "
      rows.append(row)
      index -= 1

    template = open(str(config.RESOURCES_DIR.joinpath("readme.template")), 'r',
                    encoding="utf-8").read()
    readme_data = template.format(submission_placeholder="\n".join(rows))
    with open(self.readme_path, 'w', encoding="utf-8") as fp:
      fp.write(readme_data)
