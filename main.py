from utils import clustering, parse_to_ES, processing, convert_response_to_df
from esclient import _get_client


# main pipeline
def pipeline(nl):
    cluster = clustering(nl)
    body = parse_to_ES(cluster)
    es = _get_client()
    response = es.search(index='real_estate', body=body)
    
    return processing(response, cluster)


if __name__ == '__main__':
    x = pipeline("Draw me a price chart Apartment in HaNoi according to district")
    print(x)