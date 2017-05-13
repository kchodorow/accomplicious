def _impl(ctx):
    ctx.action(
        inputs = [ctx.file.app],
        outputs = [ctx.outputs.executable],
        command = """
echo 'FLASK_DEBUG=1 FLASK_APP=%s flask run' > %s
""" % (ctx.file.app.short_path, ctx.outputs.executable.path))

    return struct(
        runfiles = ctx.runfiles(ctx.files.data + ctx.files.srcs),
    )

flask = rule(
    implementation = _impl,
    attrs = {
        'app' : attr.label(
            single_file = True,
            allow_files = True,
        ),
        'srcs' : attr.label_list(allow_files = [".py"]),
        'data' : attr.label_list(),
    },
    executable = True,
)
