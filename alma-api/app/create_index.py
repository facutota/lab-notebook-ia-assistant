import os
from dotenv import load_dotenv
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)

load_dotenv()

endpoint   = os.getenv("AZURE_SEARCH_ENDPOINT")
key        = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(key))

index = SearchIndex(
    name=index_name,
    fields=[
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True
        ),

        # Campo grande: SOLO searchable
        SearchField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True
        ),

        # Metadata (sí pueden ser filterable)
        SimpleField(
            name="title",
            type=SearchFieldDataType.String,
            filterable=True
        ),
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True
        ),
        SimpleField(
            name="domain",
            type=SearchFieldDataType.String,
            filterable=True
        ),

        # Vector
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=3072,
            vector_search_profile_name="vector-profile",
        ),
    ],
    vector_search=VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config",
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(name="hnsw-config")
        ]
    ),
)

print(f"Creando índice: {index_name} ...")
client.create_index(index)
print("Índice creado OK.")