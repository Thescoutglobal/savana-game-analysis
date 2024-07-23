## Savana AI
Welcome to the Savana AI development environment! This guide will help you set up Savana on your local machine and contribute to its development.

## Introduction
Savana is a sports analytics tool that leverages sports science and state-of-the-art AI capabilities to analyze player performance across various sports. In this repository, we implement Savana's ability to make complex inferences from sports videos we receive.

## Setup 
Clone this repository into your local environment using the following command:

```git
git clone https://github.com/Thescoutglobal/savana-game-analysis.git
```

### Tools
The development of Savana leverages the following tools:
* <b>YOLO:</b> State-of-the-art statistical model
* <b>OPEN CV:</b> For computer vision
* <b>PANDAS:</b> Data framing
* <b>NUMPY:</b> Mathematical computations
* <b>SUPERVISION:</b> Object tracking algorithms

### Installation
<b>Note:</b> The implementation of Savana AI heavily relys on ```OpenCV``` for computer vision operations and ```YOLOv5``` for statistical modeling and inferencing. It requires Python 3.7 or higher. Ensure you have at least Python 3.7 installed on your system.

To install the tools required for this project, run the following command from the root directory of this project:


On Windows:

```cmd
pip install -r requirements.txt
``` 
On MacOS and Linux

```bash
pip3 install -r requirements.txt
``` 

### Execution
This project can be exceuted from a terminal using the following command:

On Windows:
```cmd
python main.py <media path>
```

On MacOS and Linux:
```bash
python3 main.py <media path>
```
<b>Where:</b> <i>media path:</i> is the path of video to analyse

## Contribution
If you can access this repository from your account, it means you can contribute to our codebase. To minimize conflicts with other contributors, we discourage direct pushes to the main branch. Contributors should create feature branches for specific tasks. When the implementation is complete, create a pull request for code review before merging.


<b>NOTE:</b> 
- Code reviewers may request changes before merging. 
- Resolve conflicts between your feature branch and the main branch before creating a pull request.
- Avoid pushing files and directories that are specific to your development environment to the main branch (e.g., cache files, code editor settings, test media files, outputs, environment variables, etc). Include such files in a ```.gitignore``` file to prevent interfering with other contributors' development environments.
- Use descriptive commit messages to help others follow understand what was done for that commit.

### Thank You for Helping Make Savana A SOTA Sports Inference Tool