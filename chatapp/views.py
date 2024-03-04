# from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chatbotapi.settings import *

from .models import *

# Create your views here.

# Here is user chat limit

User_chat_limit = 5


class StartConvUserView(APIView):

    def get(self, request):
        print("check the api key is here ", Open_AI_API_KEY)
        print("get method is called", request.data)
        data = request.data
        if data.get("ip"):
            print("in if condition")
            if UserDataLog.objects.filter(user_ip=str(data.get("ip"))).exists():
                user_conve_check = UserDataLog.objects.get(user_ip=str(data.get("ip")))
                print("user_conve_check.limit", user_conve_check.limit)
                if user_conve_check.limit < User_chat_limit:
                    return Response(
                        {"msg": "Start Conversation"}, status=status.HTTP_200_OK
                    )
                else:
                    print("chec email and phone", user_conve_check.phone)
                    print("chec email and phone", user_conve_check.email)

                    if user_conve_check.phone and user_conve_check.email:
                        print("in if conditions")
                        return Response(
                            {"msg": "Conversation limit reached"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        print("in else conditions")
                        return Response(
                            {"msg": "Conversation limit reached", "ask": "User Data"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
            else:
                user = UserDataLog(user_ip=str(data.get("ip")))
                user.save()
                return Response(
                    {"msg": "Start Conversation"}, status=status.HTTP_200_OK
                )
        else:
            print("end else conditions")
            return Response(
                {"msg": "Need user Ip address "}, status=status.HTTP_400_BAD_REQUEST
            )


import os
import warnings

import openai
from langchain import OpenAI, VectorDBQA
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS


class StartChat(APIView):

    def post(self, request):
        print(request.data)
        data = request.data
        if data.get("ip") and data.get("ques"):
            get_user_ip = data.get("ip")
            get_user_questions = data.get("ques")
            user_details = UserDataLog.objects.get(user_ip=get_user_ip)
            if user_details.limit < User_chat_limit:
                # Conve ML Part is here

                warnings.filterwarnings("ignore")

                def get_intent(user_input):
                    prompt = f"""
                    Analyze the following user input and determine the most likely purchase intent of the user and return only intent name from given option. The user said:
                    '{user_input}'

                    Possible Intents:
                    - greeting
                    - goodbye
                    - other_intent
                    - initiate_contact_or_schedule_meeting
                    Based on the user input, the most likely intent is:
                    Intent:"""

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                    )
                    intent = response.choices[0].message["content"].strip()
                    print(intent)
                    return intent

                def get_response(intent, user_query):
                    if intent == "other_intent":
                        custom_prompt = """
                        Use the following pieces of context to answer the question at the end. Please provide
                        a answer only. If you don't know the answer or if it's not present in given context, don't try to make up an answer,
                        Context: {context}
                        Question: {question}
                        Helpful Answer:
                        """

                        custom_prompt_template = PromptTemplate(
                            template=custom_prompt,
                            input_variables=["context", "question"],
                        )

                        llm = OpenAI(
                            model_name="gpt-3.5-turbo-instruct",
                            temperature=0,
                            openai_api_key=openai.api_key,
                        )
                        file_path = os.path.join(
                            os.path.dirname(__file__), "GNS Prices.txt"
                        )
                        doc_loader = TextLoader(file_path)
                        documents = doc_loader.load()

                        text_splitter = CharacterTextSplitter(chunk_overlap=0)
                        texts = text_splitter.split_documents(documents)

                        embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
                        docsearch = FAISS.from_documents(texts, embeddings)
                        retriever = docsearch.as_retriever(
                            search_type="similarity", search_kwargs={"k": 2}
                        )

                        custom_qa = RetrievalQA.from_chain_type(
                            llm=llm,
                            chain_type="stuff",
                            retriever=retriever,
                            return_source_documents=False,
                            chain_type_kwargs={"prompt": custom_prompt_template},
                        )
                        return custom_qa.run(user_query)

                def collect_user_consent():
                    consent = input(
                        "Bot: Do you consent to us collecting and using your contact information for the purpose of scheduling a meeting and providing further assistance? (yes/no) "
                    )
                    return consent.lower() == "yes"

                def handle_data_protection(email, phone):
                    # Implement measures to securely store and handle the data
                    # For example, encrypting the data and storing it in a secure database
                    pass

                def delete_user_data(email, phone):
                    # Implement functionality to delete user data upon request
                    # This might involve removing the data from your database
                    pass

                def collect_contact_info():
                    print(
                        "Bot: To assist you further, may I have your contact information?"
                    )
                    email = input("Bot: Please enter your email address: ")
                    phone = input("Bot: Please enter your phone number: ")
                    return email, phone

                def schedule_meeting():
                    # Replace the URL below with the actual scheduling link
                    scheduling_link = "https://www.yourcompany.com/schedule-meeting"
                    print(
                        f"Bot: Thank you! You can schedule a meeting with our staff here: {scheduling_link}"
                    )

                def main():
                    # openai.api_key = (
                    #     "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"
                    # )
                    print("in conver api key is here ", Open_AI_API_KEY)
                    openai.api_key = Open_AI_API_KEY
                    print(
                        "Bot: Hello! Welcome to GNS CPAs. How can I assist you today?\nOptions: Accounting, Tax, Audit, Bookkeeping, Payroll"
                    )

                    # interaction_count = 0
                    # end_conversation = False
                    # while interaction_count < 3 and not end_conversation:
                    # user_input = input("User: ")
                    print("user input is here check", get_user_questions)
                    intent = get_intent(get_user_questions)

                    if intent == "goodbye":
                        print("Bot: Thank you for visiting GNS CPAs. Have a great day!")
                        print("First elif condition is working....")
                        end_conversation = True
                        response = "Thank you for visiting GNS CPAs. Have a great day!"
                        return response
                    elif intent == "greeting":
                        # response = get_response(intent, get_user_questions)
                        print("Bot: Hello! How I can help you?")
                        print("second elif condition is working....")
                        response = "Hello! How I can help you?"
                        print(f"Bot: {response}")
                        return response
                    elif intent == "initiate_contact_or_schedule_meeting":
                        print("third elif condition is working....")
                        response = "ask data to user"
                        return response
                        # consent_given = collect_user_consent()
                        # if consent_given:
                        #     email, phone = collect_contact_info()
                    else:
                        print("+1 limit")
                        response = get_response(intent, get_user_questions)
                        print(f"Bot: {response}")
                        user_details.limit += 1
                        user_details.save()
                        return response
                        # interaction_count += 1

                bot_ans = main()

                if bot_ans == "ask data to user":
                    print("in if condition is working")
                    return Response(
                        {"msg": "Answer of the questions", "ask": "User Data"},
                        status=status.HTTP_200_OK,
                    )

                print("process the question is here")

                return Response(
                    {"msg": "Answer of the questions", "Answer": bot_ans},
                    status=status.HTTP_200_OK,
                )
            else:

                print("user data is here also", user_details)
                print("user data is here also", user_details.email)
                print("user data is here also", user_details.phone)

                if user_details.email and user_details.phone:
                    print("in if conditions")
                    return Response(
                        {"msg": "Conversation limit reached"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                else:
                    print("in else conditions")
                    return Response(
                        {"msg": "Conversation limit reached", "ask": "User Data"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        else:
            return Response(
                {"msg": "Need user Ip address and ques both"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDataSave(APIView):
    def post(self, request):
        data = request.data
        if data.get("ip") and data.get("email") and data.get("phone"):
            get_user_ip = data.get("ip")
            print("chekc ip ", get_user_ip)
            userdata = UserDataLog.objects.get(user_ip=get_user_ip)
            print("check the user datad a", userdata.limit)
            if userdata.limit <= User_chat_limit:
                userdata.email = str(data.get("email"))
                userdata.phone = str(data.get("phone"))
                userdata.save()
                scheduling_link = "https://www.yourcompany.com/schedule-meeting"
                print(
                    f"Bot: Thank you! You can schedule a meeting with our staff here: {scheduling_link}"
                )
                return Response(
                    {
                        "msg": "User Data save successfully",
                        "ans": f"Thank you! You can schedule a meeting with our staff here: {scheduling_link}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"msg": "Need user Ip address, email and phone"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserDatareset(APIView):
    def post(self, request):
        data = request.data
        if data.get("ip"):
            userdata = UserDataLog.objects.get(user_ip=str(data.get("ip")))
            userdata.limit = 0
            userdata.save()
            return Response(
                {"msg": "limit reset done"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(
                {"msg": "Need user Ip address"},
                status=status.HTTP_400_BAD_REQUEST,
            )
