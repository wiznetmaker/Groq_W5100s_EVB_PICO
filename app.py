from machine import Pin, SPI
import network
import utime
import urequests

def init_ethernet(timeout=10):
    spi = SPI(0, 2_000_000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
    nic = network.WIZNET5K(spi, Pin(17), Pin(20))
    nic.active(True)

    start_time = utime.ticks_ms()
    while not nic.isconnected():
        if (utime.ticks_diff(utime.ticks_ms(), start_time) > timeout * 1000):
            raise Exception("Ethernet connection timed out.")
        utime.sleep(1)
        print('Connecting ethernet...')
    print(f'Ethernet connected. IP: {nic.ifconfig()}')

def send_chat_request(api_key, user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": user_message}],
        "model": "llama3-70b-8192"
    }

    start_time = utime.ticks_ms()  # 시작 시간 기록

    response = urequests.post(url, headers=headers, json=payload)
    elapsed_time = utime.ticks_diff(utime.ticks_ms(), start_time)  # 경과 시간 계산

    if response.status_code == 200:
        try:
            content = response.json()['choices'][0]['message']['content']
            return content, elapsed_time  # 내용과 처리 시간 반환
        except Exception as e:
            raise Exception("Failed to decode JSON from response: " + str(e))
    else:
        raise Exception(f"API error ({response.status_code}): {response.reason}")

def main():
    api_key = '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'
    init_ethernet()

    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        elif not user_input:
            continue

        try:
            response_content, time_taken = send_chat_request(api_key, user_input)
            print(f"LLaMA Response: {response_content} (Processed in {time_taken} ms)")  # 내용과 시간 출력
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    main()