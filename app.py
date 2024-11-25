# app.py  
import streamlit as st  
import streamlit_authenticator as stauth    
from src import db, models, utils, project, sprint, task, knowledge_base  
import pandas as pd  
import datetime  
import yaml  
from yaml.loader import SafeLoader  
import copy  
  
import random    
  
def get_tag_color(tag):    
    random.seed(tag)  # Ensure the same tag always gets the same color    
    r = lambda: random.randint(0,255)    
    return f'#{r():02X}{r():02X}{r():02X}'    
  
# Initialize database  
models.initialize_database()  
  
st.set_page_config(page_title="Team Project Manager", layout='wide')  
  
# --- User Authentication ---  
def main():  
    # Load configuration from YAML file  
    # with open('.streamlit/screts.yaml') as file:  
    #     config = yaml.load(file, Loader=SafeLoader)  

    # # Make a deepcopy of the credentials to make it mutable  
    # credentials = copy.deepcopy(config['credentials'])  

    # # Create the authenticator object  
    # authenticator = stauth.Authenticate(  
    #     credentials=credentials,  
    #     cookie_name=config['cookie']['name'],  
    #     key=config['cookie']['key'],  
    #     cookie_expiry_days=config['cookie']['expiry_days'],  
    #     preauthorized=config.get('preauthorized'),  
    #     prehashed=True  # Set to True if passwords are pre-hashed  
    # ) 
  
    # Render the login widget  
    #name, authentication_status, username = authenticator.login(location='main')  
    # try:
    #     #name, authentication_status, username = 
    #     authenticator.login(key='Login', location='main')
    #     print(st.session_state['name'], st.session_state['authentication_status'], st.session_state['username'])
    #     st.session_state['authentication_status'] = True
    # except Exception as e:
    #     st.error(e)

    # if st.session_state['authentication_status']:
    #     run_app('turan')
    #authenticator.login(key='Login', location='main')
    st.session_state['authentication_status']=True
    st.session_state['name'] = "Turan"

    if st.session_state['authentication_status']==True:  
        st.sidebar.success(f"Welcome {st.session_state['name']}!")  
        run_app(st.session_state['name'])  
    elif st.session_state['authentication_status'] == False:  
        st.error('Username/password is incorrect')  
    elif st.session_state['authentication_status'] == None:  
        st.warning('Please enter your username and password') 
  
    # if authentication_status:  
    #     # Proceed with the main app if authentication is successful  
    #     run_app(name, authenticator)  
    # elif authentication_status == False:  
    #     st.error('Username/password is incorrect')  
    # elif authentication_status == None:  
    #     st.warning('Please enter your username and password') 
  
def run_app(name):
    st.sidebar.success(f"Welcome {name}!")  
  
    # Add a logout button  
    #authenticator.logout('Logout', 'sidebar')  
  
    # Proceed with your main app code  
    # Check if edit mode is initiated    
    if 'edit_mode' not in st.session_state:    
        st.session_state['edit_mode'] = False    
    if 'edit_task_id' not in st.session_state:    
        st.session_state['edit_task_id'] = None   
  
    # Sidebar Navigation  
    menu = ["Dashboard", "Projects", "Add Task", "Sprints", "Knowledge Base"]  
    choice = st.sidebar.selectbox("Menu", menu)  
  
    # Implement functionality based on user's choice  
    if choice == "Dashboard":    
        st.title("Project Dashboard")  
        df_tasks = task.get_all_tasks()  
        projects_df = project.get_all_projects()  
    
        if projects_df.empty:  
            st.warning("No projects found. Please create a project first.")  
        else:  
            # Project Selection  
            project_options = ["All Projects"] + projects_df['name'].tolist()  #projects_df['name'].tolist()  
            project_selection = st.selectbox("Select Project", project_options)  
            if project_selection == "All Projects":  
                project_tasks = df_tasks  
            else:  
                project_id = projects_df.loc[projects_df['name'] == project_selection, 'id'].values[0]  
                project_id = int(project_id)  
                project_tasks = df_tasks[df_tasks['project_id'] == project_id]
            #project_id = projects_df.loc[projects_df['name'] == project_selection, 'id'].values[0]  
            #project_id = int(project_id)  # Ensure project_id is a Python int  
            #project_tasks = df_tasks[df_tasks['project_id'] == project_id]
    
            if project_tasks.empty:  
                st.info(f"No tasks found for project '{project_selection}'.")  
            else:  
                # Sprint Selection  
                sprints_df = sprint.get_all_sprints()  
                sprint_options = ["All Sprints"] + sprints_df['name'].tolist()  
                sprint_selection = st.selectbox("Select Sprint", sprint_options)  
    
                if sprint_selection != "All Sprints":  
                    sprint_id = sprints_df.loc[sprints_df['name'] == sprint_selection, 'id'].values[0]  
                    sprint_id = int(sprint_id)
                    filtered_tasks = project_tasks[project_tasks['sprint_id'] == sprint_id]  
                else:  
                    filtered_tasks = project_tasks  
    
                if filtered_tasks.empty:  
                    st.info(f"No tasks found for the selected sprint.")  
                else:  
                    # --- Add Download Button Here ---  
                    # Convert the filtered tasks DataFrame to CSV string  
                    csv_data = filtered_tasks.to_csv(index=False)  
    
                    # Add a download button  
                    st.download_button(  
                        label="Download Tasks as CSV",  
                        data=csv_data,  
                        file_name="tasks.csv",  
                        mime="text/csv"  
                    )  
                    # --- End of Download Button Section --- 
                    
                    # Implement the Board View  
                    st.write(f"### Tasks for Project: {project_selection}, Sprint: {sprint_selection}")  
                    statuses = ["To Do", "In Progress", "Review", "Done"]  
                    tab_labels = statuses  
                    tabs = st.tabs(tab_labels)  
                    
                    for tab, status in zip(tabs, statuses):  
                        with tab:  
                            st.markdown(f"#### {status}")  
                            status_tasks = filtered_tasks[filtered_tasks['status'] == status]  
                            if status_tasks.empty:  
                                st.write("No tasks in this status")  
                            else:  
                                for _, task_row in status_tasks.iterrows():  
                                    # Use project's color for the border  
                                    border_color = task_row['project_color'] if 'project_color' in task_row and task_row['project_color'] else '#000000'
                                    with st.expander(task_row['title'], expanded=False):  
                                        # Apply border color using HTML and CSS  
                                        st.markdown(  
                                            f"""  
                                            <div style='border: 2px solid {border_color}; padding: 8px; border-radius: 5px;'>  
                                                <p><strong>Project:</strong> {task_row['project_name']}</p>  
                                                <p><strong>Description:</strong> {task_row['description']}</p>  
                                                <p><strong>Sprint:</strong> {task_row['sprint_name'] if task_row['sprint_name'] else 'Unassigned'}</p>  
                                                <p><strong>Created At:</strong> {task_row['created_at']}</p>  
                                            </div>  
                                            """,  
                                            unsafe_allow_html=True  
                                        )
                                        # st.write(f"**Description:** {task_row['description']}")  
                                        # st.write(f"**Tags:** {task_row['tags']}")  
                                        # st.write(f"**Sprint:** {task_row['sprint_name'] if task_row['sprint_name'] else 'Unassigned'}")  
                                        # st.write(f"**Created At:** {task_row['created_at']}")  
                                        edit, delete = st.columns([1, 1])  
                                        if edit.button("Edit", key=f"edit_{task_row['id']}"):  
                                            st.session_state['edit_task_id'] = task_row['id']  
                                            st.session_state['edit_mode'] = True  
                                            st.rerun()  
                                        if delete.button("Delete", key=f"delete_{task_row['id']}"):  
                                            task.delete_task(task_row['id'])  
                                            st.success(f"Task '{task_row['title']}' deleted successfully.")
                                            st.rerun()  
                    # status_columns = st.columns(len(statuses))  
                    # for idx, status in enumerate(statuses):  
                    #     with status_columns[idx]:  
                    #         st.markdown(f"#### {status}")  
                    #         status_tasks = filtered_tasks[filtered_tasks['status'] == status]  
                    #         for _, task_row in status_tasks.iterrows():  
                    #             with st.expander(task_row['title'], expanded=False):  
                    #                 st.write(f"**Description:** {task_row['description']}")  
                    #                 st.write(f"**Tags:** {task_row['tags']}")  
                    #                 st.write(f"**Sprint:** {task_row['sprint_name'] if 'sprint_name' in task_row and task_row['sprint_name'] else 'Unassigned'}")  
                    #                 st.write(f"**Created At:** {task_row['created_at']}")  
                    #                 edit, delete = st.columns([1, 1])  
                    #                 if edit.button("Edit", key=f"edit_{task_row['id']}"):  
                    #                     # Implement edit functionality  
                    #                     pass  
                    #                 if delete.button("Delete", key=f"delete_{task_row['id']}"):  
                    #                     task.delete_task(task_row['id'])  
                    #                     st.success(f"Task '{task_row['title']}' deleted successfully.")  
                                        

        # If in edit mode, display the edit task form  
        if st.session_state['edit_mode']:  
            st.subheader("Edit Task")  
            task_id = st.session_state['edit_task_id']  
            task_df = df_tasks[df_tasks['id'] == task_id]  
            if not task_df.empty:  
                task_to_edit = task_df.iloc[0]  
                with st.form(key='edit_task_form'):  
                    title = st.text_input("Title", value=task_to_edit['title'])  
                    description = st.text_area("Description", value=task_to_edit['description'])  
                    status = st.selectbox("Status", ["To Do", "In Progress", "Review", "Done"], index=["To Do", "In Progress", "Review", "Done"].index(task_to_edit['status']))  
                    tags = st.text_input("Tags (comma-separated)", value=task_to_edit['tags'])  
                    # Project selection  
                    project_options = projects_df['name'].tolist()  
                    current_project_name = task_to_edit['project_name']  
                    if current_project_name in project_options:  
                        project_index = project_options.index(current_project_name)  
                    else:  
                        project_index = 0  # Default to first project if not found
                    project_selection = st.selectbox("Assign to Project", project_options, index=project_index)  
                    project_id = int(projects_df.loc[projects_df['name'] == project_selection, 'id'].values[0]) 
                    # Sprint selection  
                    active_sprints = sprint.get_all_sprints(active_only=True)  
                    sprint_options = ["None"] + active_sprints['name'].tolist()  
                    current_sprint_name = task_to_edit['sprint_name'] if task_to_edit['sprint_name'] else "None"  
                    if current_sprint_name in sprint_options:  
                        sprint_index = sprint_options.index(current_sprint_name)  
                    else:  
                        sprint_index = 0  # Default to "None" if not found  
                    sprint_selection = st.selectbox("Assign to Sprint", sprint_options, index=sprint_index)  
                    sprint_id = None  
                    if sprint_selection != "None":  
                        sprint_id = int(active_sprints.loc[active_sprints['name'] == sprint_selection, 'id'].values[0])  
                    submit = st.form_submit_button("Update Task")  
                    if submit:  
                        task.update_task(task_id, title, description, status, tags, project_id, sprint_id)  
                        st.success(f"Task '{title}' updated successfully!")  
                        # Reset edit mode  
                        st.session_state['edit_mode'] = False  
                        st.session_state['edit_task_id'] = None  
                        st.rerun()  
            else:  
                st.error("Task not found.") 

    elif choice == "Projects":  
        st.subheader("Project Management")  
        project_menu = ["View Projects", "Add Project", "Project Timeline"]  
        project_choice = st.sidebar.selectbox("Project Options", project_menu)  
    
        if 'edit_project_mode' not in st.session_state:  
            st.session_state['edit_project_mode'] = False  
        if 'edit_project_id' not in st.session_state:  
            st.session_state['edit_project_id'] = None  
    
        if project_choice == "View Projects":  
            projects_df = project.get_all_projects()  
            if projects_df.empty:  
                st.info("No projects available.")  
            else:  
                for _, project_row in projects_df.iterrows():  
                    st.write(f"### {project_row['name']}")  
                    st.write(f"**Description:** {project_row['description']}")  
                    st.write(f"**Start Date:** {project_row['start_date']}")  
                    st.write(f"**Estimated End Date:** {project_row['estimated_end_date']}")  
                    project_tasks = task.get_all_tasks()  
                    project_tasks = project_tasks[project_tasks['project_id'] == project_row['id']]  
                    st.write(f"**Number of Tasks:** {len(project_tasks)}")  
                    edit, delete = st.columns([1, 1])  
                    if edit.button("Edit", key=f"edit_project_{project_row['id']}"):  
                        st.session_state['edit_project_id'] = project_row['id']  
                        st.session_state['edit_project_mode'] = True  
                        st.rerun()  
                    if delete.button("Delete", key=f"delete_project_{project_row['id']}"):  
                        # Implement project deletion logic (handle foreign key constraints)  
                        st.warning("Project deletion not implemented yet.")  
                    st.markdown("---")  
    
            # If in edit mode, display the edit project form  
            if st.session_state['edit_project_mode']:  
                st.subheader("Edit Project")  
                project_id = st.session_state['edit_project_id']  
                project_df = projects_df[projects_df['id'] == project_id]  
                if not project_df.empty:  
                    project_to_edit = project_df.iloc[0]  
                    with st.form(key='edit_project_form'):  
                        project_name = st.text_input("Project Name", value=project_to_edit['name'])  
                        project_description = st.text_area("Project Description", value=project_to_edit['description'])  
                        project_start_date = st.date_input("Start Date", value=pd.to_datetime(project_to_edit['start_date']))  
                        project_estimated_end_date = st.date_input("Estimated End Date", value=pd.to_datetime(project_to_edit['estimated_end_date']))  
                        project_color = st.color_picker("Project Color", value=project_to_edit['color'] or "#000000") 
                        submit = st.form_submit_button("Update Project")  
                        if submit:  
                            project.update_project(project_id, project_name, project_description, project_start_date, project_estimated_end_date, project_color)  
                            st.success(f"Project '{project_name}' updated successfully!")  
                            st.session_state['edit_project_mode'] = False  
                            st.session_state['edit_project_id'] = None  
                            st.rerun()  
                else:  
                    st.error("Project not found.")  
        elif project_choice == "Add Project":  
            with st.form(key='add_project_form'):  
                project_name = st.text_input("Project Name")  
                project_description = st.text_area("Project Description")  
                project_start_date = st.date_input("Start Date")  
                project_estimated_end_date = st.date_input("Estimated End Date")  
                project_color = st.color_picker("Project Color", value="#000000")
                submit = st.form_submit_button("Create Project")  
                if submit:  
                    project.create_project(project_name, project_description, project_start_date, project_estimated_end_date, project_color)  
                    st.success(f"Project '{project_name}' created successfully!")  
                    st.rerun()  

        if project_choice == "Project Timeline":  
            projects_df = project.get_all_projects()  
            if projects_df.empty:  
                st.info("No projects available.")  
            else:  
                # Prepare data for Gantt chart  
                import plotly.express as px  
    
                projects_df['Start'] = pd.to_datetime(projects_df['start_date'])  
                projects_df['Finish'] = pd.to_datetime(projects_df['estimated_end_date'])  
                projects_df['Project'] = projects_df['name']  
        
                # Use the 'color' column for coloring projects  
                fig = px.timeline(  
                    projects_df,  
                    x_start="Start",  
                    x_end="Finish",  
                    y="Project",  
                    color='Project',  # Color by project name  
                    color_discrete_map={row['name']: row['color'] for _, row in projects_df.iterrows()},  
                    title="Project Timeline"  
                )
                fig.update_yaxes(autorange="reversed")  # Reverse the y-axis to have the first project at the top  
                fig.update_layout(showlegend=False)  # Hide legend if desired  
                st.plotly_chart(fig)   

    elif choice == "Add Task":  
        st.subheader("Add New Task")  
        with st.form(key='add_task_form'):  
            title = st.text_input("Title")  
            description = st.text_area("Description")  
            status = st.selectbox("Status", ["To Do", "In Progress", "Review", "Done"])  
            tags = st.text_input("Tags (comma-separated)")  
            # Project selection  
            projects_df = project.get_all_projects()  
            project_options = projects_df['name'].tolist()  
            if not project_options:  
                st.warning("Please create a project first.")  
                st.stop()  
            project_selection = st.selectbox("Assign to Project", project_options)  
            project_id = projects_df.loc[projects_df['name'] == project_selection, 'id'].values[0]  
            project_id = int(project_id)  # Ensure project_id is a Python int  
            # Sprint selection  
            active_sprints = sprint.get_all_sprints(active_only=True)  
            sprint_options = ["None"] + active_sprints['name'].tolist()  
            sprint_selection = st.selectbox("Assign to Sprint", sprint_options)  
            submit = st.form_submit_button("Add Task")  
            if submit:  
                sprint_id = None  
                if sprint_selection != "None":  
                    sprint_id = active_sprints.loc[active_sprints['name'] == sprint_selection, 'id'].values[0]  
                    sprint_id = int(sprint_id)  # Ensure sprint_id is a Python int  
                task.create_task(title, description, status, tags, project_id, sprint_id)  
                st.success(f"Task '{title}' added successfully!")  

    elif choice == "Sprints":  
        st.subheader("Sprint Management")  
        sprint_menu = ["View Sprints", "Create Sprint"]  
        sprint_choice = st.sidebar.selectbox("Sprint Options", sprint_menu)  
    
        if 'edit_sprint_mode' not in st.session_state:  
            st.session_state['edit_sprint_mode'] = False  
        if 'edit_sprint_id' not in st.session_state:  
            st.session_state['edit_sprint_id'] = None  
    
        if sprint_choice == "View Sprints":  
            sprints_df = sprint.get_all_sprints()  
            if sprints_df.empty:  
                st.info("No sprints available.")  
            else:  
                for _, sprint_row in sprints_df.iterrows():  
                    st.write(f"### {sprint_row['name']}")  
                    st.write(f"**Start Date:** {sprint_row['start_date']}")  
                    st.write(f"**End Date:** {sprint_row['end_date']}")  
                    st.write(f"**Status:** {'Active' if sprint_row['is_active'] else 'Closed'}")  
    
                    tasks_df = sprint.get_sprint_tasks(sprint_row['id'])  
                    st.write(f"**Tasks in this Sprint:** {len(tasks_df)}")  
    
                    if not tasks_df.empty:  
                        st.dataframe(tasks_df[['id', 'title', 'status', 'tags']])  
    
                    edit, close = st.columns([1, 1])  
                    if edit.button("Edit", key=f"edit_sprint_{sprint_row['id']}"):  
                        st.session_state['edit_sprint_id'] = sprint_row['id']  
                        st.session_state['edit_sprint_mode'] = True  
                        st.rerun()  
                    if sprint_row['is_active']:  
                        if close.button("Close Sprint", key=f"close_sprint_{sprint_row['id']}"):  
                            sprint.close_sprint(sprint_row['id'])  
                            st.success(f"Sprint '{sprint_row['name']}' closed.")  
                            st.rerun()  
                    st.markdown("---")  
    
            # If in edit mode, display the edit sprint form  
            if st.session_state['edit_sprint_mode']:  
                st.subheader("Edit Sprint")  
                sprint_id = st.session_state['edit_sprint_id']  
                sprint_df = sprints_df[sprints_df['id'] == sprint_id]  
                if not sprint_df.empty:  
                    sprint_to_edit = sprint_df.iloc[0]  
                    with st.form(key='edit_sprint_form'):  
                        sprint_name = st.text_input("Sprint Name", value=sprint_to_edit['name'])  
                        start_date = st.date_input("Start Date", value=pd.to_datetime(sprint_to_edit['start_date']))  
                        end_date = st.date_input("End Date", value=pd.to_datetime(sprint_to_edit['end_date']))  
                        is_active = st.checkbox("Is Active", value=bool(sprint_to_edit['is_active']))  
                        submit = st.form_submit_button("Update Sprint")  
                        if submit:  
                            sprint.update_sprint(sprint_id, sprint_name, start_date, end_date, int(is_active))  
                            st.success(f"Sprint '{sprint_name}' updated successfully!")  
                            st.session_state['edit_sprint_mode'] = False  
                            st.session_state['edit_sprint_id'] = None  
                            st.rerun()  
                else:  
                    st.error("Sprint not found.")  
        elif sprint_choice == "Create Sprint":  
            with st.form(key='create_sprint_form'):  
                sprint_name = st.text_input("Sprint Name")  
                start_date = st.date_input("Start Date")  
                end_date = st.date_input("End Date")  
                submit = st.form_submit_button("Create Sprint")  
                if submit:  
                    sprint.create_sprint(sprint_name, start_date, end_date)  
                    st.success(f"Sprint '{sprint_name}' created successfully!")  
                    st.rerun()

    elif choice == "Knowledge Base":  
        st.subheader("Knowledge Base")
        kb_menu = ["View Entries", "Add Entry"]
        kb_choice = st.sidebar.selectbox("Options", kb_menu)
        
        if kb_choice == "View Entries":
            entries_df = knowledge_base.get_all_knowledge_entries()
            if entries_df.empty:
                st.info("No knowledge base entries available.")
            else:
                # Optionally filter by project
                projects_df = project.get_all_projects()
                project_options = ["All Projects"] + projects_df['name'].tolist()
                project_selection = st.selectbox("Filter by Project", project_options)
                if project_selection != "All Projects":
                    project_id = projects_df.loc[projects_df['name'] == project_selection, 'id'].values[0]
                    project_id = int(project_id) 
                    entries_df = entries_df[entries_df['project_id'] == project_id]
                for index, entry in entries_df.iterrows():
                    with st.expander(entry['title'], expanded=False):
                        st.write(f"**Project:** {entry['project_name']}")
                        st.write(f"**Tags:** {entry['tags']}")
                        st.markdown(entry['content'])
        elif kb_choice == "Add Entry":
            with st.form(key='add_kb_form'):
                title = st.text_input("Title")
                # Project selection
                projects_df = project.get_all_projects()
                project_options = projects_df['name'].tolist()
                if not project_options:
                    st.warning("Please create a project first.")
                    st.stop()
                project_selection = st.selectbox("Assign to Project", project_options)
                project_id = projects_df.loc[projects_df['name'] == project_selection, 'id'].values[0]
                project_id = int(project_id) 
                tags = st.text_input("Tags (comma-separated)")
                content = st.text_area("Content (Markdown Supported)")
                submit = st.form_submit_button("Add Entry")
                if submit:
                    knowledge_base.add_knowledge_entry(title, content, tags, project_id)
                    st.success(f"Knowledge entry '{title}' added successfully!")
                    st.rerun()
  
if __name__ == "__main__":  
    main()  
