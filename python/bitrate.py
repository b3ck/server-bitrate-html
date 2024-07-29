import obspython as obs
import urllib.request
import urllib.error
import json
import xml.etree.ElementTree as ET
from time import sleep
from threading import Thread, Event

# --- Global Variables ---

source_name = ""
server_type = "SRT"
url = ""
key = ""
enable_rtt = False
interval = 2000
show_kbps = True
show_separator = True
separator_char = "•"
enable_logging = True  # Add this variable to control logging
thread = None
fetching_data = Event()
is_fetching = False

# --- Console Logging ---

def log_to_console(message):
    if enable_logging:
        obs.script_log(obs.LOG_INFO, message)

def log_error(message):
    if enable_logging:
        obs.script_log(obs.LOG_ERROR, message)

# --- Button Handling ---

def toggle_button_pressed(props, prop):
    try:
        global thread, is_fetching
        if not fetching_data.is_set():
            fetching_data.set()
            is_fetching = True
            thread = Thread(target=fetch_bitrate)
            thread.daemon = True
            thread.start()
            log_to_console("Starting data fetching.")
        else:
            fetching_data.clear()
            is_fetching = False
            log_to_console("Stopping data fetching.")
        update_button_text(props)
    except Exception as e:
        log_error(f"Error in toggle_button_pressed: {e}")
    return True

def update_button_text(props):
    try:
        button = obs.obs_properties_get(props, "toggle_button")
        if is_fetching:
            obs.obs_property_set_description(button, "Stop")
        else:
            obs.obs_property_set_description(button, "Start")
    except Exception as e:
        log_error(f"Error in update_button_text: {e}")

# --- Script Properties ---

def script_properties():
    try:
        props = obs.obs_properties_create()

        button_group = obs.obs_properties_create()
        obs.obs_properties_add_group(
            props, "button_group", "Control", obs.OBS_GROUP_NORMAL, button_group
        )

        obs.obs_properties_add_button(
            button_group, "toggle_button", "Start", toggle_button_pressed
        )

        text_source_list = obs.obs_properties_add_list(
            props,
            "source_name",
            "Text Source",
            obs.OBS_COMBO_TYPE_EDITABLE,
            obs.OBS_COMBO_FORMAT_STRING,
        )
        populate_text_sources(text_source_list)
        server_list = obs.obs_properties_add_list(
            props,
            "server_type",
            "Server Type",
            obs.OBS_COMBO_TYPE_LIST,
            obs.OBS_COMBO_FORMAT_STRING,
        )
        obs.obs_property_list_add_string(server_list, "SRT", "SRT")
        obs.obs_property_list_add_string(server_list, "RIST", "RIST")
        obs.obs_property_list_add_string(server_list, "NMS", "NMS")
        obs.obs_property_list_add_string(server_list, "NGINX", "NGINX")
        obs.obs_properties_add_text(props, "url", "URL", obs.OBS_TEXT_DEFAULT)
        obs.obs_properties_add_text(
            props, "key", "Key (if applicable)", obs.OBS_TEXT_DEFAULT
        )

        obs.obs_properties_add_bool(props, "enable_rtt", "Enable RTT (for SRT/RIST)")
        obs.obs_properties_add_int(
            props, "interval", "Update Interval (ms)", 500, 10000, 100
        )
        obs.obs_properties_add_bool(props, "show_kbps", "Show 'KB/s'")
        obs.obs_properties_add_bool(props, "show_separator", "Show Separator")
        obs.obs_properties_add_text(
            props, "separator_char", "Separator Character", obs.OBS_TEXT_DEFAULT
        )
        obs.obs_properties_add_bool(props, "enable_logging", "Enable Logging")  # Add this line

        update_button_text(props)
        log_to_console("Properties created.")
        return props
    except Exception as e:
        log_error(f"Error in script_properties: {e}")

def populate_text_sources(prop):
    try:
        sources = obs.obs_enum_sources()
        if sources:
            for source in sources:
                source_id = obs.obs_source_get_id(source)
                if source_id in ["text_gdiplus_v2", "text_ft2_source_v2"]:
                    name = obs.obs_source_get_name(source)
                    obs.obs_property_list_add_string(prop, name, name)
            obs.source_list_release(sources)
        log_to_console("Text sources populated.")
    except Exception as e:
        log_error(f"Error in populate_text_sources: {e}")

def script_update(settings):
    try:
        global source_name, server_type, url, key, enable_rtt, interval, show_kbps, show_separator, separator_char, enable_logging

        source_name = obs.obs_data_get_string(settings, "source_name")
        server_type = obs.obs_data_get_string(settings, "server_type")
        url = obs.obs_data_get_string(settings, "url")
        key = obs.obs_data_get_string(settings, "key")
        enable_rtt = obs.obs_data_get_bool(settings, "enable_rtt")
        interval = obs.obs_data_get_int(settings, "interval")
        show_kbps = obs.obs_data_get_bool(settings, "show_kbps")
        show_separator = obs.obs_data_get_bool(settings, "show_separator")
        separator_char = obs.obs_data_get_string(settings, "separator_char")
        enable_logging = obs.obs_data_get_bool(settings, "enable_logging")  # Add this line

        log_to_console(
            f"Settings updated: source_name={source_name}, server_type={server_type}, url={url}, key={key}, enable_rtt={enable_rtt}, interval={interval}, show_kbps={show_kbps}, show_separator={show_separator}, separator_char={separator_char}, enable_logging={enable_logging}"
        )
    except Exception as e:
        log_error(f"Error in script_update: {e}")

def fetch_bitrate():
    try:
        while fetching_data.is_set():
            try:
                if not url:
                    log_to_console("URL is not set. Skipping fetch.")
                    sleep(interval / 1000)
                    continue

                if server_type == "SRT":
                    bitrate, rtt = get_srt_bitrate(url, key)
                elif server_type == "RIST":
                    bitrate, rtt = get_rist_bitrate(url)
                elif server_type == "NMS":
                    bitrate, rtt = get_nms_bitrate(url), None
                elif server_type == "NGINX":
                    bitrate, rtt = get_nginx_bitrate(url, key), None
                else:
                    bitrate, rtt = None, None

                update_text_source(bitrate, rtt)
            except Exception as e:
                log_error(f"Error fetching bitrate: {e}")

            sleep(interval / 1000)
    except Exception as e:
        log_error(f"Error in fetch_bitrate: {e}")

def get_srt_bitrate(url, publisher):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if publisher not in data["publishers"]:
                return None, None
            bitrate = data["publishers"][publisher]["bitrate"]
            rtt = data["publishers"][publisher].get("rtt") if enable_rtt else None
            return bitrate, rtt
    except urllib.error.URLError as e:
        log_error(f"Error fetching SRT bitrate: {e}")
        return None, None

def get_rist_bitrate(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            if "receiver-stats" not in data or data["receiver-stats"] is None:
                return None, None
            br_value = sum(
                round(peer["stats"]["bitrate"] / 1024)
                for peer in data["receiver-stats"]["flowinstant"]["peers"]
                if "bitrate" in peer["stats"]
            )
            rtt_value = next(
                (
                    round(peer["stats"]["rtt"])
                    for peer in data["receiver-stats"]["flowinstant"]["peers"]
                    if "rtt" in peer["stats"]
                ),
                None,
            )
            return br_value, rtt_value
    except urllib.error.URLError as e:
        log_error(f"Error fetching RIST bitrate: {e}")
        return None, None

def get_nms_bitrate(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data["bitrate"]
    except urllib.error.URLError as e:
        log_error(f"Error fetching NMS bitrate: {e}")
        return None

def get_nginx_bitrate(url, key):
    try:
        with urllib.request.urlopen(url) as response:
            root = ET.fromstring(response.read())
            
            # Log the XML for debugging purposes
            log_to_console(ET.tostring(root, encoding='utf8').decode('utf8'))
            
            # Iterate through all applications
            for app in root.findall('.//application'):
                live = app.find('live')
                if live is None:
                    continue
                
                # Iterate through all streams within the live section
                for stream in live.findall('stream'):
                    stream_name = stream.find('name')
                    if stream_name is not None and stream_name.text == key:
                        bw_in = stream.find('bw_in')
                        if bw_in is not None:
                            bitrate = int(bw_in.text) // 1024  # Convert to kbps
                            return bitrate
            
            log_error(f"Stream with key '{key}' not found.")
            return None
    except urllib.error.URLError as e:
        log_error(f"Error fetching NGINX bitrate: {e}")
        return None

def update_text_source(bitrate, rtt):
    try:
        source = obs.obs_get_source_by_name(source_name)
        if source:
            settings = obs.obs_data_create()
            if bitrate is not None:
                text = f"{bitrate}"
                if show_kbps:
                    text += " kb/s"
                if rtt is not None and show_separator:
                    text += f" {separator_char} {rtt} RTT"
            else:
                text = ""

            obs.obs_data_set_string(settings, "text", text)
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.obs_source_release(source)
            # log_to_console(f"Text source updated: {text}")
    except Exception as e:
        log_error(f"Error in update_text_source: {e}")

def script_load(settings):
    try:
        log_to_console("Script loaded and ready.")
    except Exception as e:
        log_error(f"Error in script_load: {e}")

def script_unload():
    try:
        global fetching_data
        fetching_data.clear()
        log_to_console("Script unloaded and fetching stopped.")
    except Exception as e:
        log_error(f"Error in script_unload: {e}")
