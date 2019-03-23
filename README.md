# changelog_data
data collection scripts that matches changelog.com data to GitHub project data

# How to use
1. rename local_settings.py.template to local_settings.py
2. Open local_settings.py and replace your GitHub credentials with appropriate values
3. import the functions from utils.py and fetch the data

# Requirements
Install the following packages using pip:
- requests-html
- python-dateutil
- pytz
- pandas

# Sample
See the [changelog_notebook](./changelog_notebook.ipynb) for example on how functions were used to collect data then store as CSV

**Note:** you can view jupyter notebooks on GitHub!

# How to improve this work

The main functions are in utils.py. You can clone this work and re-use and send a pull request for any improvements you make.
You can also review utils.py and add comments by clicking on the line numbers to open issues.

# How to cite this work

You are welcome to reuse and adapt this work for your own project, we ask that you reference this work in your project.

At the moment, this is part of the following working paper, cite it as:

```AlMarzouq, M., AlZaidan, A., & AlDallal, J. (2019). Realizing the Promise of Mining GitHub for Social Research. Working paper.```

We would appreciate any comments on how to best cite this work. Should the repository be cited? or the research paper that introduced the instrument? One problem that needs to be addressed is how improvements can be recognized? We can certainly add an AUTHORS file, but just like survey instrument, we hope that there can be a way in which improvements can be recognized in research papers.
