<<<<<<< HEAD
# EducationalWeb

The following instructions have been tested with Python2.7 on Linux and MacOS

1. You should have ElasticSearch installed and running -- https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html

2. Create the index in ElasticSearch by running `python create_es_index.py` from `EducationalWeb/`

3. Download tfidf_outputs.zip from here -- https://drive.google.com/file/d/19ia7CqaHnW3KKxASbnfs2clqRIgdTFiw/view?usp=sharing
   
   Unzip the file and place the folder under `EducationalWeb/static`

4. Download cs410.zip from here -- https://drive.google.com/file/d/1Xiw9oSavOOeJsy_SIiIxPf4aqsuyuuh6/view?usp=sharing
   
   Unzip the file and place the folder under `EducationalWeb/pdf.js/static/slides/`
   
5. From `EducationalWeb/pdf.js/build/generic/web` , run the following command: `gulp server`

6. In another terminal window, run `python app.py` from `EducationalWeb/`

7. The site should be available at http://localhost:8096/

=======
# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.
>>>>>>> e8480b22d6dbd62fe3fc07cb2d3837401e1c171b
