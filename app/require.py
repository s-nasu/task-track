import pkg_resources

# 作成する requirements.txt ファイルの名前
output_file = "requirements.txt"

# すべてのインストールされた配布物を取得
dists = {dist.key: dist for dist in pkg_resources.working_set}

# 他の配布物によって要求されている全てのパッケージを取得
required_by_others = {
    required.key for dist in dists.values() for required in dist.requires()
}

# トップレベルの配布物だけを抽出
top_level = set(dists) - required_by_others

# requirements.txt ファイルを開いて書き込みます
with open(output_file, "w") as f:
    for dist_name in sorted(top_level):
        # パッケージ名とバージョンを組み合わせて取得
        dist_version = dists[dist_name].version
        # ファイルに "パッケージ名==バージョン" 形式で書き込む
        f.write(f"{dist_name}=={dist_version}\n")

print(f"'{output_file}' にトップレベルのパッケージを書き込みました。")
