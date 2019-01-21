from email import message_from_file

from sys import stdin


def extract_text(msg):
    return msg.get_payload()


def get_payload(msg):
    """
    Get the payload from the Message.
    email.message.Message.get_payload will be a list of Message objects when
    is_multipart() is True, or a string when is_multipart() is False
    https://docs.python.org/3.4/library/email.message.html#email.message.Message.get_payload

    @param msg An email.message.Message
    @return str
    """
    payload = msg.get_payload()
    return '\n'.join(get_payload(m) for m in payload) if msg.is_multipart() else payload


def get_message_body(fp):
    """
    Parse a raw email message and return just the body.
    @param fp the file-like object to read
    @return a string containing the message body
    """
    msg = message_from_file(fp)
    return(get_payload(msg))


def main():
    """
    Extract an email message body from stdin and print the result to stdout.
    """
    body = get_message_body(stdin)
    print(body)


if __name__ == "__main__":
    main()
