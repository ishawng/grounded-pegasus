# Grounded PEGASUS
Using Abstractive Summarization Techniques to Infer Machine Instructions

## Directory Structure
- Cleaned datasets can be found in the `/datasets` folder.
- Dataloader code, accuracy evaluation code, and the "main" Colab notebook can be found in `/src`. 
- Scripts used for processing and pickling data for use in the Colab notebook can be found in the root directory.

## Dependency Installation and Running
- Dependencies can be found listed in the first cell of the Colab notebook.
- To perform analysis on a text-to-text model's math word problem answering ability, upload the notebook to a JupyterLab server like Colab along with the required pickled data       sources. For an easier task, use the nonnumeric SVAMP.pkl. For a harder task, use the unfiltered SVAMP.pkl.
- Upload the model for evaluation into the notebook and run through all the cells. If you encounter a runtime error you probably haven't ctrl-F-replaced enough instances of the     variable name storing the model. 
