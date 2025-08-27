from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class LLMWrapper:
    """
    Universal LLM wrapper to support multiple providers & models
    """
    SUPPORTED_PROVIDERS = {
        "groq": "langchain_groq.ChatGroq",
        "openai": "langchain_openai.ChatOpenAI",
        # Add future providers here
    }

    def __init__(self, provider="groq", api_key=None, model_name=None, temperature=0.2):
        self.provider = provider.lower()
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.chain = None  # delay init until credentials are valid

        if self.api_key and self.model_name:
            self.chain = self._init_chain()

    def _import_class(self, path: str):
        """Dynamically import class from a string path"""
        module_name, class_name = path.rsplit(".", 1)
        mod = __import__(module_name, fromlist=[class_name])
        return getattr(mod, class_name)

    def _init_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are TalentScout Assistant. ONLY return valid JSON, no explanations."),
            ("user", "{question}")
        ])

        if self.provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"❌ Unsupported provider: {self.provider}")

        LLMClass = self._import_class(self.SUPPORTED_PROVIDERS[self.provider])

        if self.provider == "groq":
            llm = LLMClass(
                groq_api_key=self.api_key,
                model_name=self.model_name,
                temperature=self.temperature,
                streaming=True,
            )
        elif self.provider == "openai":
            llm = LLMClass(
                openai_api_key=self.api_key,
                model_name=self.model_name,
                temperature=self.temperature,
                streaming=True,
            )

        return prompt | llm | StrOutputParser()

    def stream(self, question: str):
        if not self.chain:
            raise RuntimeError("⚠️ Chain not initialized. Please provide API key and model.")
        return self.chain.stream({"question": question})

    def validate(self) -> bool:
        """
        Check if the API key and model are valid by making a tiny test call.
        Returns True if it works, False otherwise.
        """
        if not self.chain:
            return False

        try:
            # Just send a simple ping
            resp = "".join([c for c in self.chain.stream({"question": "ping"})])
            return bool(resp.strip())
        except Exception:
            return False
