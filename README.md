     _ _____                                _ _           
    (_)  ___|                              | (_)          
     _\ `--.  ___  _ __ ___  _ __ ___   ___| |_  ___ _ __ 
    | |`--. \/ _ \| '_ ` _ \| '_ ` _ \ / _ \ | |/ _ \ '__|
    | /\__/ / (_) | | | | | | | | | | |  __/ | |  __/ |   
    |_\____/ \___/|_| |_| |_|_| |_| |_|\___|_|_|\___|_|   
                                                      
    ------------------------------------------------------

Team Members
------
John Markese  
Rebecca “Rui” Lu 
Sunitha Vijayanarayan 

### About iSommelier:
Using a wine review dataset retrieved from Kaggle our project is to create a user interface that that allows searching and filtering through a 130K record dataset of wine attributes, descriptions, and reviews. The engine would serve as a resource for wine enthusiasts to find detailed information about wines from across the globe and also contribute their own wines and reviews. 
Looking for the perfect wine for your Friday night date? Well, iSommelier is the place to go to select the perfect pairing for your Foie Gras. Who needs the highbrow wine experts, when iSommelier is faster and less intimidating?

Many of the existing wine review websites are in a blog or forum format or require a subscription to browse the content, and we are looking to provide an interface that allows more intuitive and robust searching than what a blog/forum platform provides while being openly available the public.

### Usefulness:
The iSommelier is the perfect platform for wine enthusiasts to read about and discover new wines without the pressure of consulting with experts. It also provides a platform for the public to share their own experiences and reviews and keep track of their favorites.

### Dataset:
The dataset that fuels iSommelier is a 130K record dataset from Kaggle that contains a vast amount of wine information, including basic geographic data, pricing, tasting notes, ratings, and wine reviews. Since the dataset is de-normalized, some processing and data-cleansing will necessary to convert it to a relation model, and the objective of the project is to supplement the Kaggle wine review data with iSommelier’s own community content.
https://www.kaggle.com/zynicide/wine-reviews

### Functionality:
Initially, having an interface that wraps queries and inserts into the dataset is the baseline of what we are going to provide. For example, a SELECT statement with any need JOINs will be necessary along with performance enhancing indices to find a particular wine according to the user’s criteria. Additionally, any INSERTs, UPDATEs, and DELETEs might best be contained within a database transaction that adhere to any referential integrity constraints and perhaps use cascading deletes. Another potential feature is to provide the user some data visualizations in the form of graphs or geographic visuals. iSommelier will also implement a Natural Language Processing (NLP) engine that allows users to interact with the content of the reviews in a more intuitive way. These additional features might make the use of views, stored procedures, or other RDBMS features.
Basic Functions:
-	CRUD features for new iSommelier community content
-	Query for wine reviews
Advanced Functions:
-	Natural Language Processing (NLP)
-	Data Visualization
Advanced Techniques: TBD
