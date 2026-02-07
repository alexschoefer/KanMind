<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>KanMind – Project Management Backend</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<h1>KanMind</h1>

<p>
    <strong>KanMind</strong> is a backend API for a project management tool built with
    <em>Django</em> and <em>Django REST Framework</em>.
</p>

<p>
    With KanMind, you develop the complete backend logic for a modern project
    management application. The frontend is provided separately – your responsibility
    is to ensure that all background processes, data handling, and permissions
    work reliably and seamlessly together with the frontend.
</p>

<p>
    The API enables users to manage boards, tasks, and comments while enforcing
    role-based access control and authentication.
</p>

<hr>

<h2>🚀 Features</h2>
<ul>
    <li>User registration and token-based authentication</li>
    <li>Board creation with owners and members</li>
    <li>Task management with status and priority</li>
    <li>Assignment and review workflow for tasks</li>
    <li>Comment system for tasks</li>
    <li>Permission-based access control</li>
</ul>

<hr>

<h2>🛠 Tech Stack</h2>
<ul>
    <li>Python 3</li>
    <li>Django</li>
    <li>Django REST Framework</li>
    <li>Token Authentication</li>
    <li>SQLite (development)</li>
</ul>

<hr>

<h2>📦 Installation</h2>

<h3>1. Clone the repository</h3>
<pre>
git clone https://github.com/alexschoefer/KanMind.git
cd KanMind
</pre>

<h3>2. Create and activate a virtual environment</h3>
<pre>
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
</pre>

<h3>3. Install dependencies</h3>
<pre>
pip install -r requirements.txt
</pre>

<h3>4. Apply migrations</h3>
<pre>
python manage.py migrate
</pre>

<h3>5. Run the development server</h3>
<pre>
python manage.py runserver
</pre>

<hr>

<h2>🔐 Authentication</h2>

<p>
    KanMind uses <strong>token-based authentication</strong>.
    After successful registration or login, the API returns an authentication token.
</p>

<p>Include the token in the request headers:</p>

<pre>
Authorization: Token your_token_here
</pre>

<hr>

<h2>📚 API Overview</h2>

<h3>Authentication</h3>
<table>
    <tr>
        <th>Method</th>
        <th>Endpoint</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>POST</td>
        <td>/api/register/</td>
        <td>Register a new user</td>
    </tr>
    <tr>
        <td>POST</td>
        <td>/api/login/</td>
        <td>Login and receive auth token</td>
    </tr>
</table>

<h3>Boards</h3>
<table>
    <tr>
        <th>Method</th>
        <th>Endpoint</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>GET</td>
        <td>/api/boards/</td>
        <td>List boards the user owns or is a member of</td>
    </tr>
    <tr>
        <td>POST</td>
        <td>/api/boards/</td>
        <td>Create a new board</td>
    </tr>
    <tr>
        <td>GET</td>
        <td>/api/boards/&lt;id&gt;/</td>
        <td>Retrieve board details</td>
    </tr>
    <tr>
        <td>PATCH</td>
        <td>/api/boards/&lt;id&gt;/</td>
        <td>Update board data</td>
    </tr>
    <tr>
        <td>DELETE</td>
        <td>/api/boards/&lt;id&gt;/</td>
        <td>Delete board (owner only)</td>
    </tr>
</table>

<h3>Tasks</h3>
<table>
    <tr>
        <th>Method</th>
        <th>Endpoint</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>POST</td>
        <td>/api/tasks/</td>
        <td>Create a new task</td>
    </tr>
    <tr>
        <td>GET</td>
        <td>/api/tasks/&lt;id&gt;/</td>
        <td>Retrieve task details</td>
    </tr>
    <tr>
        <td>PATCH</td>
        <td>/api/tasks/&lt;id&gt;/</td>
        <td>Update task</td>
    </tr>
    <tr>
        <td>DELETE</td>
        <td>/api/tasks/&lt;id&gt;/</td>
        <td>Delete task</td>
    </tr>
</table>

<hr>

<h2>🔐 Permission Concept</h2>
<ul>
    <li>Only authenticated users can access the API</li>
    <li>Only board members can access tasks and comments</li>
    <li>Only board owners can delete boards</li>
    <li>Tasks can only be deleted by their creator or the board owner</li>
    <li>Comments can only be edited or deleted by their author</li>
</ul>

<hr>

<h2>📄 License</h2>
<p>
    This project was created for educational purposes and as a demonstration
    of backend development using Django REST Framework.
</p>

</body>
</html>
