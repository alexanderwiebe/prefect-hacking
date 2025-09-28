#!/usr/bin/env python
# coding: utf-8

# # New Sprint Doc flow
# 
# The following notebook covers the steps to copy a confluence doc, rename it and then send out some slack messages.

# In[1]:


from prefect import flow, task, get_run_logger
import requests


# In[2]:


@task
def set_variables():
    return {
        "doc_name": "Sprint Success Challenges",
        "template_id": "TEMPLATE-123"
    }


# In[3]:


@task
def copy_template(template_id: str):
    # REST call to copy doc template
    return {"doc_id": "DOC-123"}


# In[4]:


@task
def rename_doc(doc_id: str, doc_name: str):
    # REST call to rename document
    # Simulate duplicate problem
    if doc_name == "Sprint Success Challenges":
        raise ValueError("Duplicate document exists")
    return {"doc_id": doc_id}


# In[5]:


@task
def delete_duplicate(doc_id: str):
    # API call to delete duplicate
    return True


# In[6]:


@task
def find_correct_doc():
    # API call to find the right doc
    return {"doc_id": "DOC-456"}


# In[7]:


@task
def send_slack_update(doc_id: str):
    print(f"Slack: New document created with id {doc_id}")


# In[8]:


@task
def send_congrats():
    print("Slack: Congrats! 🎉")


# # Main Flow

# In[9]:


@flow
def sprint_success_flow():
    logger = get_run_logger()

    vars = set_variables()
    doc_id = None

    try:
        # Step 1 – copy and rename
        copied = copy_template(vars["template_id"])
        renamed = rename_doc(copied["doc_id"], vars["doc_name"])
        doc_id = renamed["doc_id"]

    except Exception as e:
        logger.warning(f"Error during rename: {e}")
        delete_duplicate(copied["doc_id"])
        corrected = find_correct_doc()
        doc_id = corrected["doc_id"]

    # Step 2 – notify in Slack
    send_slack_update(doc_id)
    send_congrats()

