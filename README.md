# By Tomorrow

A project supporting researchers in doing thorough preparation on a short time horizon, like *by tomorrow before the meeting*.

Currently supports making author profiles in markdown, which can either be consumed directly (eg in a jupyter notebook) or uploaded to [NotebookLM](https://notebooklm.google.com/) to prompt/query for summary info or other details.

## Author Profiles

### Setup Repo
This repo relies on rye as a package manager in place of pip.  You can install rye by following [these quickstart instructions](https://notebooklm.google.com/).  Then you should be able to just clone the repo and ask rye to sync.

```shell
# clone the repo
cd by_tomorrow
rye sync
# after this the repo should be setup
```

Then, the suggested method for interacting currently is a jupyter notebook.  You'll need to run it with rye for the dependencies to work:
```shell
rye run jupyter-lab
```

The path structure described below expects the notebook to be created in the `by_tomorrow/notebooks/` directory.

### Setup Config & Filepaths

The repo uses [hydra](https://hydra.cc/) for config management.  The only value you need to change in the config, `configs/paper_data.yaml` shown below, is the data_dir.  You can change it directly in the ipynb.

```yaml
───────┬────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: configs/paper_data.yaml
───────┼────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ # Directories
   2   │ data_dir: /Users/daniellerothermel/drotherm/data/
   3   │
   4   │ raw_pdf_dir: ${data_dir}raw_pdfs/
   5   │ parsed_pdf_dir: ${data_dir}parsed_pdfs/
   6   │ metadata_dir: ${data_dir}parsed_pdfs/
   7   │ author_data_dir: ${data_dir}author_data/
   8   │ author_summaries_dir: ${author_data_dir}summaries/
   9   │
  10   │ # Re File names
  11   │ author_info_file: ${author_data_dir}manual_profiles.json
  12   │
  13   │ # Patterns
  14   │ prof_pattern: (?P<professor_name>[\w_]+)
  15   │ file_type_pattern: (?P<file_type>\w+)
  16   │ version_pattern: v(?P<version>\d+)
  17   │
  18   │ author_summary_file_pattern: ${prof_pattern}\.${file_type_pattern}\.${version_pattern}
  19   │
  20   │
───────┼────────────────────────────────────────────────────────────────────────────────────────────────────
```

First, setup the config at the top of the jupyter notebook:
```python
import hydra
from omegaconf import DictConfig, OmegaConf
from hydra import initialize, compose

import bytom.author_profiles as ap

with initialize(config_path="../configs/", version_base=None):
    cfg = compose(config_name="paper_data.yaml")

# Update the data dir path
cfg.data_dir = # TODO: YOUR PATH HERE!!!

cfg_resolved = OmegaConf.to_container(cfg, resolve=True)
print(f"Configuration: \n\n{OmegaConf.to_yaml(cfg_resolved)}")
```

Then, the author profile code expects you to manually find bio data for the author.  This can be done by just copying the info on their personal page.  For example:
```python
author_info = {
	"He He": """
I want to build intelligent systems that can communicate with humans effectively and enable individuals to achieve their goals. Today's systems are often opaque, brittle, and difficult to control, which limits their usefulness in human-centered applications. To make them our trustworthy collaborators, my research aims to (i) understand the computational foundation of generalization in novel scenarios, and (ii) build interactive systems that align with user's goals.

I am an Assistant Professor of Computer Science and Center for Data Science at New York University. I am affiliated with the CILVR Lab, the Machine Learning for Language Group, and the Alignment Research Group.

Here are some directions I'm excited about nowadays:

- Robustness: Machine learning models are trained on a fixed and often biased dataset, but face a constantly-changing world. How can we build predictors that align with human rationales, avoid spurious correlations, and generalize to out-of-distribution data? How can models adapt quickly given new information?
- Truthfulness: We are increasingly relying on machine learning models (e.g., large language models) for critical tasks. How can we make sure that the model outputs conform to facts? Does the model know what it doesn\u2019t know? Can it output a \u201cproof\u201d for its answer? How do we evaluate factuality efficiently for questions beyond the ability of an average person?
- Human-AI collaboration: We want AI agents to deal with our daily minutiae, support our decision-making, and teach us complex concepts. How should the agent infer user intention and preferences, allow for fine-grained control, and take (natural language) feedback? How will this collaboration shape the future workforce?
	""",
}
```

### Creating the Author Page
```python
# Create the pages
author_pages = {}
for author, author_bio in author_info.items():
    author_pages[author] = make_author_page(
        cfg,
        author,
        responses=None,        # This will query the arxiv api
        author_info=author_bio,
        max_papers=3,          # The max papers to return, ordered by recency
        max_years=2,           # Only return papers in the last 2 years
        first_last_only=True,  # Only return papers where the author is first or last author
    )

# Then you can display them directly in the notebook
from IPython.display import Markdown, display
display(Markdown(author_pages['He He']))

# And then you can dump the results to load with NotebookLM
import dr_util.file_utils as fu
fu.dump_file(author_pages['He He'], f"{cfg.author_summaries_dir}he_he.markdown.v0.txt")
```

An example of how the papers are displayed:

### **Title:** GOODAT: Towards Test-time Graph Out-of-Distribution Detection
	
**Publish Date:** 2024-01-10
	
**First Author:** Luzhi Wang
	
**Last Author:** Tat-Seng Chua
	
**Middle Authors:** Dongxiao He, He Zhang, Yixin Liu, Wenjie Wang, Shirui Pan, Di Jin
	
**Abstract:** Graph neural networks (GNNs) have found widespread application in modeling graph data across diverse domains. While GNNs excel in scenarios where the testing data shares the distribution of their training counterparts (in distribution, ID), they often exhibit incorrect predictions when confronted with samples from an unfamiliar distribution (out-of-distribution, OOD). To identify and reject OOD samples with GNNs, recent studies have explored graph OOD detection, often focusing on training a specific model or modifying the data on top of a well-trained GNN. Despite their effectiveness, these methods come with heavy training resources and costs, as they need to optimize the GNN-based models on training data. Moreover, their reliance on modifying the original GNNs and accessing training data further restricts their universality. To this end, this paper introduces a method to detect Graph Out-of-Distribution At Test-time (namely GOODAT), a data-centric, unsupervised, and plug-and-play solution that operates independently of training data and modifications of GNN architecture. With a lightweight graph masker, GOODAT can learn informative subgraphs from test samples, enabling the capture of distinct graph patterns between OOD and ID samples. To optimize the graph masker, we meticulously design three unsupervised objective functions based on the graph information bottleneck principle, motivating the masker to capture compact yet informative subgraphs for OOD detection. Comprehensive evaluations confirm that our GOODAT method outperforms state-of-the-art benchmarks across a variety of real-world datasets. The code is available at Github: https://github.com/Ee1s/GOODAT
	
---------------


### Notebook LM

So far I've tried uploading a single source file (bio + abstracts from recent papers) to a new notebook ([here](https://notebooklm.google.com/)).  Then I've used the following two prompts:
- "The provided source is a bio of a researcher and then a collection of his recent research papers. What are the major themes of his research, clustered, and who are his main collaborators for each?"
- "Can you decompose the themes in more detail? What are the major questions that he has asked in each theme and what are the preliminary answers and remaining open questions?"

Example results below using Prof. He, 100 papers within the last 5 years, first last only.  In the notebook they're cited and if you click on the citation it will pop up the retrieved text that was used to generate the text.  With the abstract-only representations the retrieved text is generally the description of a single paper.

**Prompt 1**
```
He He's research, as shown in the provided bio and her recent publications, can be classified into four major themes:
1. Understanding and Improving Large Language Models (LLMs)
- Focus: This research theme examines the capabilities and limitations of LLMs, particularly in reasoning, truthfulness, and generalization. It aims to understand how these models learn and how to improve their performance in real-world applications.
- Methods: He He and her collaborators use a variety of methods to study and improve LLMs. These methods include:
    - Prompt Engineering: Crafting specific prompts to elicit desired behaviors from LLMs.
    - Fine-tuning: Adapting pre-trained LLMs to specific tasks or datasets.
    - Synthetic Datasets: Creating controlled datasets to systematically analyze LLM behavior.
    - Analysis of Internal Representations: Probing the internal activations of LLMs to understand their knowledge and reasoning processes.
- Collaborators:
    - Abulhair Saparov: Co-authored multiple papers on LLM reasoning, truthfulness, and the formal analysis of chain-of-thought reasoning.
    - Nitish Joshi: Collaborated on work exploring truthfulness, causal inference, and the impact of personas in LLMs.
    - Richard Yuanzhe Pang: Worked together on understanding LLM reasoning processes, text generation techniques, and reward gaming in conditional text generation.
    - Yanda Chen: Collaborated on papers examining in-context learning, sensitivity, and the influence of parallel structures in pre-training data on ICL abilities.
    - Chen Zhao: Co-authored studies on collaborative capabilities of language models, in-context learning, and the impact of parallel structures on ICL.
    - Vishakh Padmakumar: Worked together on projects investigating content diversity in LLM-assisted writing, deductive reasoning, and creative image captioning.
    - Kathleen McKeown: Collaborated on research related to in-context learning, sensitivity, and the effect of parallel structures in pre-training data.
    - Zhou Yu: Co-authored studies on in-context learning and sensitivity.
...


2. Robustness and Generalization
...

3. Human-AI Interaction and Collaboration
...

4. Applications of Machine Learning and Natural Language Processing
...
```

**Prompt 2**
```
Deeper Exploration of He He's Research Themes
1. Understanding and Improving Large Language Models (LLMs)
- Major Questions:
    - Can LLMs reason deductively? If so, what are the limits of their reasoning abilities?
    - How do LLMs perform causal inference? Are they susceptible to fallacies?
    - How can we measure and improve the truthfulness of LLMs?
    - How do LLMs acquire in-context learning (ICL) abilities? What factors influence their ICL performance?
    - How sensitive are LLMs to variations in prompts? Can we mitigate this sensitivity?
- Preliminary Answers:
    - LLMs demonstrate some deductive reasoning capabilities but struggle with complex proofs and proof planning. They tend to be "greedy reasoners," focusing on immediately available deductions rather than exploring multiple reasoning paths.
    - LLMs can extract causal facts from text but are prone to fallacies like the post hoc fallacy, suggesting limitations in their causal understanding.
    - The truthfulness of LLMs can be influenced by factors like the presence of "(un)truthful personas" in the training data and fine-tuning on factual information.
    - Parallel structures in pre-training data significantly contribute to LLM's ICL abilities. Removing these structures leads to a substantial drop in ICL performance.
    - LLMs are highly sensitive to prompt variations, and this sensitivity negatively correlates with their accuracy.
- Open Questions:
    - How can we enhance LLM's deductive reasoning abilities, particularly their capacity to handle complex proofs and engage in more systematic proof planning?
    - How can we improve LLM's causal reasoning to avoid fallacies and make more robust causal inferences?
    - How can we effectively evaluate and ensure the truthfulness of LLMs across a wider range of tasks and domains?
    - What are the mechanisms by which parallel structures facilitate ICL? How can we leverage this understanding to further improve ICL?
    - How can we develop techniques to make LLMs more robust to prompt variations and reduce their oversensitivity?
...
```

But, of course, there are many potential extensions both to the prompting method and to what data you use as the source!



# Dev Instructions

### Using Rye

Full deep dive: [dr_setup/repos/rye_usage.md](https://github.com/drothermel/dr_setup/blob/repo_setup/repos/rye_usage.md)

Ideally rye has already been setup:
```shell
rye init --no-readme --name PROJ_NAME REPO_PATH
rye pin 3.12
rye sync
rye show
rye list # jupyterlab, jupyterlab_vim, pytest, dr_util
```

Basic Usage:
```
rye add PACKAGE (opt: --dev) (opt: --git URL)
rye remove PACKAGE (opt: --dev)
rye fmt
rye lint --fix
rye test -v
rye run TOOL_NAME
```

### Using hydra + wandb

- Hydra deep dive: [dr_setup/repos/hydra_usage.md](https://github.com/drothermel/dr_setup/blob/repo_setup/repos/hydra_usage.md)
- Wandb deep dive: [dr_setup/repos/wandb_usage.md
](https://github.com/drothermel/dr_setup/blob/repo_setup/repos/wandb_usage.md)

Install both:
```shell
rye add wandb
rye add hydra-core==1.3
```

Use both in a script:
```python
import wandb
import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="conf", config_name="qmp_cfg")
def run(cfg: DictConfig):
  logging.info(">> Input config yaml:")
  logging.info("\n" + str(OmegaConf.to_yaml(cfg)))
	
  cfg_dict = OmegaConf.to_container(cfg, resolve=True)
  wandb.init(
    project='name',
    config=cfg_dict,
  )
  wandb.log({"data": 100})

if __name__ == "__main__":
  run()
```
