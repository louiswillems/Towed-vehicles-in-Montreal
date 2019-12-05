
# Visualizing Towed vehicles in Montreal

Web app tutorial project made with streamlit. [See the app](http://donnees.ville.montreal.qc.ca)

You can use Streamlit to create interactive Data Science pages, deployable to the web through all major deployment surfaces. 

![Current State](https://user-images.githubusercontent.com/33185528/67614707-9e50f300-f78f-11e9-9811-c817474ea571.png)

## Getting Started

Using a python3 (preferably 3.7) environment, run the following to install all the libraries used in this repository:
```
pip install -r requirements.txt
```
Recommend using conda or pipenv to sandbox your work

### Data

The [data](http://donnees.ville.montreal.qc.ca/dataset/remorquages-de-vehicules-genants/resource/e62322fb-3e14-4ee0-b724-a77190dac8e7) show vehicles towed by the City of Montreal since 2016. Towing is performed for example during snow removal, construction work or during special events.

### Manual Install 

Run:

```
streamlit run app.py
```

Note: Install all the libraries that are imported in app.py in order to succeesfully run the project.