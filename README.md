<div style="display: flex; justify-content: space-between; align-items: center;">
    <nav>
        <a href="#About Me" style="margin-right: 15px; text-decoration: none;">About Me</a>
        <a href="#Projects" style="margin-right: 15px; text-decoration: none;">Projects</a>
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
        <p>Hi there! My name is Minji Lee. I’m a Ph.D. candidate in Technology at Purdue University, specializing in Computer Vision and UAV-based Semantic Segmentation. My research focuses on developing machine learning pipelines for high-resolution aerial imagery, particularly for ecological monitoring and object-level segmentation. I’ve previously interned at LG Innotek as an AI researcher within the AI/Big Data Solutions team, where I worked on generative modeling and synthetic dataset creation. I also completed research internships at Argonne National Laboratory in both 2021 and 2022, contributing to projects in robotics and the Mathematics and Computer Science (MCS) division.</p>
    </div>
</div>

## <a id="About Me"></a>About Me

As my name suggests, I am originally from Seoul, South Korea, and I also had the opportunity to live in Japan for a time. In 2016, during my senior year as an undergraduate student, I had the privilege of visiting Purdue University as part of a visiting scholar program. That experience left a lasting impression on me, and I was excited to return to Purdue after being offered a Research Assistantship and admission to the graduate program.

For my master’s thesis, I designed an intelligent zipper robot that integrated a machine learning algorithm to determine the optimal operational threshold based on sensor data collected from individuals with physical disabilities. The system leveraged real-time input to adapt its behavior, enhancing both performance and usability for users with varying levels of physical ability. This research combined robotics, human-centered design, and algorithmic decision-making to support more inclusive assistive technologies.

## <a id="Projects"></a>Projects

My research centers on building an end-to-end machine learning pipeline for UAV-based semantic segmentation, particularly for identifying Eastern Red Cedar trees in high-resolution aerial imagery. This pipeline integrates raw data collection, preprocessing, annotation, model development, evaluation, and deployment—tailored for ecological applications where precision and scalability are critical.


### [Data Acquisition](proj/DA/README.md)
**Multimodal Semantic Segmentation of Eastern Red Cedar Trees: Integrating Visual Masks and Natural Language Prompts**

key words: Instance Segmentation, Ground Sampling Distance, Multimodal

<table style="width: 100%; table-layout: fixed;">
  <tr>
    <td style="width: 40%; height: 300px; vertical-align: top;">
      <img src="/proj/DA/mapping.png" alt="demo_erc_2" style="width: 100%; height: 100%; object-fit: contain;">
    </td>
    <td style="width: 60%; padding-left: 20px; vertical-align: top;">
        This study proposes a multimodal approach transforming instance segmentation masks into spatially grounded natural language prompts. By extracting segmented masks as a ground truth and estimating object dimensions, the system categorizes Eastern Red Cedar specimens based on their varying sizes and positions them within a 3×3 spatial grid. These attributes are subsequently translated into interpretive summaries which can suggest early-stage spread that can be addressed through immediate intervention as Agent AI. The descriptions generated support ecological decision-making by identifying removal complexity, prioritizing intervention zones, and estimating operational costs, facilitating resource allocation planning, as larger specimens require mechanical or fire-based removal strategies, while smaller individuals may be managed through manual intervention.
    </td>
  </tr>
</table>

---

### [Model Training](proj/DA/README.md)
**Exploring the Boundary Between Human-Defined Machine Learning and Data-Driven Deep Learning**

key words: Training Method, Feature Extraction

<table style="width: 100%; table-layout: fixed;">
  <tr>
    <td style="width: 40%; height: 300px; vertical-align: top;">
      <img src="/proj/DA/mask_variations.png" alt="demo_erc_2" style="width: 100%; height: 100%; object-fit: contain;">
    </td>
    <td style="width: 60%; padding-left: 20px; vertical-align: top;">
      Rule-based ML techniques often require domain expertise and are effective when feature boundaries are well understood. In contrast, DL models excel in complex, high-dimensional environments by automatically extracting relevant features, albeit at the cost of transparency and increased computational demands. Through empirical experiments, we demonstrate how each method performs under different constraints and offer insights into when one approach may be favored over the other. The findings contribute to guiding model selection strategies in data-driven research and real-world applications.
    </td>
  </tr>
</table>

---

### [Model Evaluation](proj/DA/README.md)
**CedarSAM: Fine-Tuning Segment Anything Model for Semantic Segmentation of Eastern Red Cedar Vegetation from UAV Imagery**

key words: Mask-Decoder Tuning, Vision Transformer, Semantic Segmentation

<table style="width: 100%; table-layout: fixed;">
  <tr>
    <td style="width: 40%; height: 300px; vertical-align: top;">
      <img src="/ROMAN/best_dice/sample_96_comparison.png" alt="demo_erc_2" style="width: 100%; height: 100%; object-fit: contain;">
    </td>
    <td style="width: 60%; padding-left: 20px; vertical-align: top;">
      Although the Segment Anything Model (SAM) has demonstrated remarkable generalization ability in zero-shot segmentation tasks, its performance on specialized or domain-specific imagery, such as aerial vegetation images, may fall short of the precision required for real-world applications. This study investigates the effectiveness of fine-tuning CedarSAM on a small and labeled dataset of aerial tree images to enhance segmentation performance for a specific tree species. Despite the limited dataset size, the results show that the CedarSAM model achieves notable improvements in segmentation accuracy across multiple metrics, including Dice score, IoU, Precision, Recall, and Inference time. These findings highlight the potential of domain adaptation with minimal data, enabling practitioners to deploy SAM effectively in niche applications without the need for large-scale datasets.
    </td>
  </tr>
</table>

---

### [Model Deployment](proj/DA/README.md)
**TEST**

key words: DEPLOY TEST

<table style="width: 100%; table-layout: fixed;">
  <tr>
    <td style="width: 40%; height: 300px; vertical-align: top;">
      <img src="/ROMAN/best_dice/best_dice_score_distributions.png" alt="demo_erc_2" style="width: 100%; height: 100%; object-fit: contain;">
    </td>
    <td style="width: 60%; padding-left: 20px; vertical-align: top;">
      Deployment Test with Docker.
    </td>
  </tr>
</table>

---


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

![demo_erc_4](/ROMAN/sam_figures.png)

To address this, I developed CedarSAM, a fine-tuned variant of SAM tailored to identify and segment Eastern Red Cedar (ERC) trees using high-resolution UAV imagery (5472 × 3648). The project focused on optimizing SAM with a small, custom-labeled dataset, aiming to enhance its segmentation accuracy for a single object class.

![demo_erc_4](/ROMAN/sam_examples.png)

#### Dataset & Annotation Strategy
I manually annotated 106 aerial images and video frames (20 FPS), each containing ~4 ERC trees. Unlike typical object datasets, four annotation types were generated for each image:

- Bounding Boxes

- Object Masks

- Instance Masks

- Edge Annotations

![demo_erc_4](/ROMAN/sam_images.png)

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

#### Best_Dice Examples
![demo_erc_4](/ROMAN/best_dice/best_dice_score_distributions.png)
![demo_erc_4](/ROMAN/best_dice/sample_96_comparison.png)


#### Best_Loss Examples
![demo_erc_4](/ROMAN/best_loss/sample_6_comparison.png)


## <a id="Contact"></a>Contact

If you have any questions, feel free to contact me at [lee3450@purdue.edu](mailto:lee3450@purdue.edu) or connect on [Minji Lee LinkedIn](https://www.linkedin.com/in/minji-lee-purdue/).



