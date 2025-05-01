<div style="display: flex; justify-content: space-between; align-items: center;">
    <nav>
        <a href="#About Me" style="margin-right: 15px; text-decoration: none;">About Me</a>
        <a href="#Projects" style="margin-right: 15px; text-decoration: none;">Projects</a>
        <a href="#NEWS" style="margin-right: 15px; text-decoration: none;">NEWS</a>
        <a href="#Contact" style="text-decoration: none;">Contact</a>
    </nav>
    <div>
        <a href="MinjiLee_Resume_PurdueUniversity.pdf" target="_blank">
            <img src="pdf-icon.png" alt="Download CV" title="Download CV" width="30" height="30"/>
        </a>
    </div>
</div>

<div style="display: flex; align-items: center; margin-top: 20px;">
    <div style="flex: 1; margin-right: 20px;">
        <img src="profile.jpg" alt="Profile Picture" width="200" height="auto">
    </div>
    <div style="flex: 2;">
        <p>Hi there! My name is Minji Lee. I’m a Ph.D. Candidate in Technology at Purdue University. As a deep learning engineer, I excel in the areas of computer vision, especially semantic segmentation of farming and agriculture images, performance modeling, and source code algorithm optimization. My research aims to bridge the gap between theoretical segmentation models and their practical applications through innovative design and implementation. Currently, I am working as a researcher to utilize SAM (Segment Anything Model) developed by Meta, evaluating its validity as a foundation model in comparison to traditional models such as CNNs. This evaluation aims to validate the hypothesis that SAM is also effective in specific domains. To enhance my UAV-captured dataset, I have generated synthetic images of eastern red cedar trees using diffusion models, which are integrated into the evaluation process to benchmark model performance. Feel free to reach out to me at <a href="mailto:lee3450@purdue.edu" style="color: inherit; text-decoration: none;">lee3450@purdue.edu</a> if you have any questions or would like to connect.</p>
    </div>
</div>

## <a id="About Me"></a>About Me

As my name suggests, I am originally from Seoul, South Korea, and I lived in Japan for a while. As a senior undergraduate student in 2016, I had the privilege of visiting Purdue University as part of a visiting scholar group. The experience left a lasting impression, and I was thrilled to return to Purdue after receiving an offer, largely due to the outstanding teamwork.

My master's thesis focused on designing a zipper robot integrated with a machine learning algorithm to determine the optimal threshold using sensor data collected from people with physical disabilities. The algorithm leveraged the data to enhance the robot's performance and adaptability, providing a more efficient and user-friendly experience for individuals with varying levels of physical ability.

## <a id="NEWS"></a>NEWS

- **August 2025** — Expected graduation from Purdue University with a Ph.D. in Computer and Information Technology, focused on semantic segmentation and generative AI.

- **November 2024** — Presented final Ph.D. thesis on CedarSAM, a fine-tuned model built for real-time segmentation in UAV-based ecological monitoring.

- **March 2024** — Passed Ph.D. candidacy exam, officially advancing to doctoral research phase.

- **June 2023** — Began internship at LG Innotek as a Research Aide Intern in AI Big Data Solutions, focusing on CNN-based hybrid models and YOLOv8 deployment.

- **May 2022** — Started internship at Argonne National Laboratory, automating ML pipelines and deploying Jetson Nano–based edge AI systems.

- **May 2021** — Accepted into the Ph.D. program at Purdue University.

- **May 2021** — Graduated with an M.S. in Computer and Information Technology at Purdue, specializing in multi-agent robotics.

- **May 2021** — Started virtual internship at Argonne National Laboratory, focusing on edge-cloud pipeline integration during the pandemic.

- **August 2019** — Began M.S. program at Purdue University in Multi-Agent Robotics.

## <a id="Projects"></a>Projects

- Purdue University, [Semantic Segmentation in Geographical Data Analysis](https://github.com/MINJILEE-PURDUE/erc_tree_semantic_segmentation_in_mlops)
- LG Innotek, [InnoMLOps Platform by SageMaker](https://github.com/MINJILEE-PURDUE/inno-mlops)
- Argonne National Laboratory, [Sage Project](https://github.com/waggle-sensor)

## Selected Projects

### Semantic Segmentation
In addition to my work in integrating AI and ML in agriculture and forestry, I have a keen interest in the analysis of geographical and meteorological data. This field offers rich opportunities for leveraging machine learning techniques to gain insights into various environmental phenomena and make informed decisions.

#### Research Focus

My research in this area centers around leveraging advanced machine learning models and techniques to analyze large-scale geographical and meteorological datasets. By applying data analysis methods to understand patterns, trends, and anomalies in weather and environmental data, I aim to contribute to our understanding of complex Earth systems and support decision-making processes in areas such as climate adaptation, disaster preparedness, and resource management.



### SAM Demo with HuggingFace/Gradio

![demo_erc_4](/src/final_demo.gif)

<div style="display: flex; flex-wrap: wrap; justify-content: center;">
    <img src="/src/mask_12_seg_1.png" alt="demo_erc_2" style="width: 30%; margin: 10px;">
    <img src="/src/mask_12_seg_2.png" alt="demo_erc_3" style="width: 30%; margin: 10px;">
    <img src="/src/mask_12_seg_3.png" alt="demo_erc_4" style="width: 30%; margin: 10px;">
</div>



### Recent Projects

#### Fine-Tuning Segment Anything Model (SAM) for Ecological Image Segmentation: Detecting Eastern Red Cedar Trees from UAV Imagery
I'm excited to share my recent research on improving the Segment Anything Model (SAM) for domain-specific segmentation in vegetation-rich environments. While SAM, trained on the general-purpose SA-1B dataset, demonstrates strong zero-shot capabilities, its performance often falls short in complex ecological scenes.

To address this, I developed CedarSAM, a fine-tuned variant of SAM tailored to identify and segment Eastern Red Cedar (ERC) trees using high-resolution UAV imagery (5472 × 3648). The project focused on optimizing SAM with a small, custom-labeled dataset, aiming to enhance its segmentation accuracy for a single object class.

![demo_erc_1](/src/image_012_clustering.png)

#### Dataset & Annotation Strategy
I manually annotated 106 aerial images and video frames (20 FPS), each containing ~4 ERC trees. Unlike typical object datasets, four annotation types were generated for each image:

- Bounding Boxes

- Object Masks

- Instance Masks

- Edge Annotations

These annotations supported diverse prompting strategies for SAM and significantly improved learning context.

  
![demo_erc_4](/src/results_old_12.png)

![demo_erc_4](/src/results_updated_12.png)

#### Model Optimization
Selective Fine-Tuning: Only the mask decoder was updated while keeping encoders frozen to reduce overfitting and training time.

- Loss Function: Combined Focal Loss (for class imbalance) with Dice Loss (for spatial accuracy).

- Training Framework: Implemented in PyTorch, trained over 40 epochs, with the best performance recorded at Epoch 40.


#### Results & Insights
Compared to the original SAM, CedarSAM achieved:

- +2.6% Dice Score

- +4.6% IoU

- 10% Reduction in Inference Time

Visualizations clearly demonstrated more accurate segmentation and reduced False Positives (FP) and False Negatives (FN), using confusion matrix overlays (Green = TP, Blue = FP, Red = FN).

![demo_erc_4](/src/results_001.png)
![demo_erc_4](/src/results_002.png)
![demo_erc_4](/src/results_003.png)
![demo_erc_4](/src/results_004.png)

