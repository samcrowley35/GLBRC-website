# Website for the GLBRC software engineer position

## How to run program:
1. After cloning this repository onto your local machine, make sure that Docker is running in the background.

2. Enter `docker build --tag glbrc-website .` into the command line to initialize the Docker container.

3. Enter `docker run --name glbrc-website -p 5001:5001 glbrc-website` to run the container.

4. After the previous step, click on one of the links that comes up to open the website. 

5. When prompted for a login, each one of the default username/password combinations (user1/glbrcpass, user2/glbrcpass, ...) will display the default links on the home page. Additionally you may sign up new users and their home pages will be automatically filled with the default links (Google and GLBRC).

6. When you are done using the website, enter CTRL+C on the command line to terminate the flask instance, then `docker stop glbrc-website` to stop the container.

## Notes
- For this assignment, I chose to use Python's Flask framework. Flask has built in authentication as well as a SQLite database called SQLalchemy that can take care of data storage. Data is automatically stored in the SQLalchemy database every time a user edits their links, and when a new user is created. This website is self-hosted and can be run with docker using the steps listed above.

- If you look at models.py, you can see the many-to-many relationship between User objects and Application objects. This allows Users to have a list of Application objects, making their list of links persist between sessions. 

- On the home page, links can be dragged and dropped within the table, and to navigate to the respective link, just click on the icon.

- The edit links page allows users to change the status of the pages. For example, if a user with the default links clicked on 'change status' for Google, then the Google link will not be visible on the user's home page. For non-default apps, when 'change status' is clicked, the app will be available the next time the user is at their home page.

- Thank you for your consideration and taking the time to use this website, I hope to hear back from you all soon. 

