function scrollToLatestMessage() {{
    let messages = document.getElementsByClassName('user-wrapper');
    if (messages.length > 0) {{
        let lastMessage = messages[messages.length - 1];
        lastMessage.scrollIntoView({ behavior: 'smooth' });
    }}
}}
scrollToLatestMessage();