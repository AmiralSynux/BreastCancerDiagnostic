
<h1>Breast Cancer Detection</h1>
Breast Cancer Detection Using Machine Learning
<img src="images/path-ai-machine-learning.png" alt="Machine Learning in Medicine"/>
<h2>What is Breast Cancer?</h2>
Cancer occurs when mutations take place in genes that regulate cell growth. The mutations let the cells divide and multiply in an uncontrolled, chaotic way. 
The cells keep on proliferating, producing copies that get progressively more abnormal. In most cases, the cell copies eventually end up forming a tumor.
Breast cancer occurs when a tumor originates in the breast. As breast cancer tumors mature, they may metastasize (spread) to other parts of the body. 
The primary route of metastasis is the lymphatic system which, is also the body's primary system for producing and transporting white blood cells and other 
cancer-fighting immune system cells throughout the body. Metastasized cancer cells that aren't destroyed by the lymphatic system's white blood cells move 
through the lymphatic vessels and settle in remote body locations, forming new tumors and perpetuating the disease process. Breast cancer is not just a woman's disease. 
It is quite possible for men to get breast cancer, although it occurs less frequently in men than in women.
<h2>Project Description</h2>
We tried to develop a CAD system that can facilitate the diagnosis of breast cancer, with respect to the EU recommendations and
AI techniques. In order to achieve this we trained our model with mammograms from the MIAS dataset and a part 
of the mini DDSM database.
<h2>The technique we used</h2>
The project is inspired by these publications and research papers:
<ol><li>A Preprocessing Algorithm for the CAD System of Mammograms Using the Active Contour Method: Farhan AKRAM, Jeong Heon KIM, Inteck WHOANG, and Kwang Nam CHOI
</li><li>MAMMOGRAM ANALYSIS BASED ON MACHINE LEARNING ALGORITHMS: A COMPARATIVE STUDY: S. Mohamed Malik, A. Alharbi
</li><li>Mammography Images Segmentation via Fuzzy C-mean and K-mean: Mohammed Y. Kamil, Ali Mohammed Salih
</li></ol>

The steps we  followed:
<ul>
<li>Choosing the data
</li>
<li>Preprocessing
</li><li>Feature extraction
</li><li>Training a binary classification model
</li><li>Image segmentation for tumor detection
</li>
</ul>

<h3>Choosing the data</h3>
As the MIAS dataset presented many normal mammograms, we chose to balance the 
dataset by using all 322 images from MIAS and another 93 malignant and benign mammograms 
from DDSM. Here are some of the plots we created in the incipient stage of our project in order to get a 
better understanding of the dataset and of the problem:
<img src="images/myplot1.png" alt="Resolution plot"/>
<img src="images/myplot2.png" alt="Diagnosis plot"/>
<img src="images/myplot3.png" alt="Left and right diagnosis plot"/>

