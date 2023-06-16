from urllib.parse import quote, unquote_plus, unquote


def read_large_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.rstrip('\n')

def parse_pdd_img_url():
    return

def parse_alice_img_url():
    return

def parse_qh_img_url():
    return


def parse_img_url(base_url):
    raw_url = urllib.parse.unquote(base_url)
    # 拼多多素材

    # 启航素材

    # 爱丽丝

    return 


if __name__ == '__main__':
    base_url = "https://alpha.alicdn.com/minolta/129577/0/fdc6390d0ce8125e3da246ec93d075a9.jpg_640x320.jpg?content" \
               "=%7B%2215%22%3A%7B%22attrs%22%3A%7B%22mini%22%3Afalse%2C%22value%22%3A%22O1CN016MVG2Q1k0St9q6jrG_%21" \
               "%212208759634621.jpg_400x400.jpg%22%7D%2C%22filters%22%3A%5B%7B%22attrs%22%3A%7B%22dst_rect%22%3A%5B0" \
               "%2C0%2C460.0%2C460.0%5D%2C%22src_rect%22%3A%5B0%2C0%2C398%2C398%5D%7D%2C%22type%22%3A%22copy%22%7D%5D" \
               "%7D%2C%2222%22%3A%7B%22attrs%22%3A%7B%22mini%22%3Afalse%2C%22value%22%3A%22O1CN016MVG2Q1k0St9q6jrG_" \
               "%21%212208759634621.jpg_200x200.jpg%22%7D%2C%22filters%22%3A%5B%7B%22attrs%22%3A%7B%22fill%22%3A%22" \
               "%23695B5231%22%2C%22rect%22%3A%5B0%2C0%2C568%2C389%5D%7D%2C%22type%22%3A%22mask%22%7D%2C%7B%22attrs" \
               "%22%3A%7B%22fill%22%3A%22%23695B527F%22%2C%22rect%22%3A%5B25%2C74%2C542%2C336%5D%7D%2C%22type%22%3A" \
               "%22mask%22%7D%2C%7B%22attrs%22%3A%7B%22fill%22%3A%22%232D2623FF%22%2C%22rect%22%3A%5B132%2C275%2C341" \
               "%2C52%5D%7D%2C%22type%22%3A%22mask%22%7D%5D%7D%2C%2263%22%3A%7B%22value%22%3A%22%5Cu6dd8%5Cu597d" \
               "%5Cu7269%22%7D%2C%2265%22%3A%7B%22value%22%3A%22%5Cu63a8%5Cu8350%5Cu5355%5Cu54c1%22%7D%2C%2267%22%3A" \
               "%7B%22value%22%3A%22%5Cu6dd8%5Cu5b9d%5Cu70ed%5Cu6b3e%22%7D%2C%228%22%3A%7B%22attrs%22%3A%7B%22mini%22" \
               "%3Afalse%2C%22value%22%3A%22O1CN016MVG2Q1k0St9q6jrG_%21%212208759634621.jpg_200x200.jpg%22%7D%2C" \
               "%22filters%22%3A%5B%7B%22attrs%22%3A%7B%22radius%22%3A%224%22%2C%22rect%22%3A%5B0%2C0%2C200%2C200%5D" \
               "%7D%2C%22type%22%3A%22gaussian_blur%22%7D%2C%7B%22attrs%22%3A%7B%22dst_rect%22%3A%5B0%2C0%2C1000" \
               "%2C500%5D%2C%22src_rect%22%3A%5B0%2C50%2C200%2C100%5D%7D%2C%22type%22%3A%22copy%22%7D%2C%7B%22attrs" \
               "%22%3A%7B%22fill%22%3A%22%23FFFFFF7F%22%2C%22rect%22%3A%5B0%2C0%2C1000%2C500%5D%7D%2C%22type%22%3A" \
               "%22mask%22%7D%5D%7D%7D&pid=mm_1873810155_2320450209_111953150429&channel=4&getAvatar=avatar "
    parse_url = unquote_plus(base_url)
    print(parse_url)


