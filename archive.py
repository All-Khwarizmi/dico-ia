# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Que veux-tu savoir ?")
if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
             st.markdown(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Ask LLM to extract the words that the user wants to translate
            response = llm_call(SYSTEM_PROMPT_3, prompt, MODE_NAME)
            
            # Check if the prompt is already in the system prompts file
            extract_words_system_prompt_id = check_and_add_system_prompt(SYSTEM_PROMPT_3)
            
            # Add interaction to interactions file
            add_llm_call_row(extract_words_system_prompt_id, "extract_words_call", prompt, response.choices[0].message.content, MODE_NAME )
            

            # Ask LLM if promt is complaint with the length constraint. If not, ask user to rephrase. Indeed, the LLM is trained to translate only two words at a time.
            print("prompt: ", prompt)
            response = llm_call(SYSTEM_PROMPT, prompt, MODE_NAME)

            # Check if the prompt is already in the system prompts file
            is_complaint_system_prompt_id= check_and_add_system_prompt(SYSTEM_PROMPT)
                
            # Add interaction to interactions file
            add_llm_call_row(is_complaint_system_prompt_id, "is_compliant_call", prompt, response.choices[0].message.content, MODE_NAME )            
           
            # Check if user prompt is compliant with the length constraint. Check if response contains "OUI" or "NON"
            if "OUI" in response.choices[0].message.content:
                print("OUI")
                print(response.choices[0])
                
                for response in CLIENT.chat.completions.create(
                model="nousresearch/nous-capybara-7b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT_2},
                    {"role": "user", "content": prompt} 
                    ],
                    stream=True,
                ):
                    if response.choices[0].delta is not None :
                        full_response += (response.choices[0].delta.content or "")
                        message_placeholder.markdown(full_response + "▌ ")
                message_placeholder.markdown(full_response)
            else:
                print("NON")
                print(response.choices)
                message_placeholder.markdown(MAX_LEN_ERROR_PLACEHOLDER)
                full_response = MAX_LEN_ERROR_PLACEHOLDER
                st.session_state.messages.append(
                    {
                        'role': "assistant",
                        'content': full_response
                    }
                )
   