from mlserver.codecs import StringCodec
import requests
import wikipediaapi


wiki_wiki = wikipediaapi.Wikipedia('MyMovieEval (example@example.com)', 'en')
barbie = wiki_wiki.page('Barbie_(film)').summary
oppenheimer = wiki_wiki.page('Oppenheimer_(film)').summary

inference_request = {
    "inputs": [
        StringCodec.encode_input(name='docs', payload=[barbie, oppenheimer], use_bytes=False).model_dump()
    ]
}
print(inference_request)

r = requests.post('http://0.0.0.0:8080/v2/models/doc-sim-model/infer', json=inference_request)

print(r.json())

print(f"Our movies are {round(r.json()['outputs'][0]['data'][0] * 100, 4)}% similar!")
