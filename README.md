team_project_manager/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── db.py
│   ├── models.py
│   ├── project.py
│   ├── sprint.py
│   ├── task.py
│   ├── knowledge_base.py
│   └── utils.py
├── data/
│   └── task_manager.db
└── scripts/
    ├── initialize_db.py
    └── run_app.sh


src/: A directory containing the source code modules.
__init__.py: Makes the src directory a Python package.
db.py: Handles the database connection and initialization.
models.py: Defines the data models and ORM mappings.
project.py: Contains functions and classes related to project management.
sprint.py: Contains functions and classes related to sprint management.
task.py: Contains functions and classes related to task management.
knowledge_base.py: Contains functions and classes related to the knowledge base.
utils.py: Utility functions used across the application.
data/: Directory for storing the SQLite database file.

