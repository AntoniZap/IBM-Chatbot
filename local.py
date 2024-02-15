shortnames = {
    "english" : "en",
    "gaeilge" : "ga"
}

languages = {
    "title" : {
        "en" : "Customer Review Analyser",
        "ga" : "Bota Comhrá C⁊F IBM",
    },
    "subheader" : {
        "en" : "Select options in sidebar.",
        "ga" : "Roghnaigh roghanna ar an dtaobhbharra."
    },
    "llm_choice_combo" : {
        "en" : "Select LLM:",
        "ga" : "Roghnaigh LLM:"
    },
    "loading" : {
        "en" : "Loading…",
        "ga" : "ag lódáil…"
    },
    "prompt_placeholder" : {
        "en" : "Write your question...",
        "ga" : "Clóscríobh do theachtaireacht..."
    },
    "user_role_label" : {
        "en" : "User",
        "ga" : "Tusa"
    },
    "assistant_role_label" : {
        "en" : "Assistant",
        "ga" : "Bota"
    },
    "llm_not_available" : {
        "en" : "Unfortunately {llm_selection}'s LLM is not available at the moment.",
        "ga" : "Faraor, níl MML {llm_selection} ar fáil faoi láthair."
    },
    "system_prompt" : {
        "en" : "You are a helpful assistant. Answer all questions to the best of your ability with the following context:",
        "ga" : "Is Bota Comhrá cabhrach tú. Freagair gach ceist leis an eolas thíos:",
    },
    "select_language" : {
        "en" : "Select language:",
        "ga" : "Roghnaigh teanga:"
    },
    "select_llm": {
        "en" : "Select LLM:",
        "ga" : "Roghnaigh LLM:",
    },
    "sources" : {
        "en" : "Sources",
        "ga" : "foinsí"
    }
}

def resolve(language, key):
    variations = languages[key]
    language = language.lower()
    if language in key:
        return variations[language]
    elif language in shortnames:
        return variations[shortnames[language]]
    else:
        raise RuntimeError(f"Language `{language}` does not exist!")
        
