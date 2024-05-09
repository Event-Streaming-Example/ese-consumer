from components.datasource.backend.configs import BackendDSConfig



def get_backend_ds_config(ctx) -> BackendDSConfig: 
    ctx.markdown("##### Backend Server Configuration")
    proto_col, base_col, end_col, freq_col = ctx.columns([1,2,2,1])

    protocol  = proto_col.selectbox("Protocol", ("http", "https"))
    base_url  = base_col.text_input("Base URL", placeholder="localhost", value="192.168.29.191")
    endpoint  = end_col.text_input("GET Endpoint", placeholder="/events", value="/events")
    frequency = freq_col.number_input("Polling frequency", value=5)

    return BackendDSConfig(protocol, base_url, endpoint, frequency)