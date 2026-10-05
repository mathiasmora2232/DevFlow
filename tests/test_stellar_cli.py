from devflow.cli import build_parser


def test_stellar_management_commands_parse():
    parser = build_parser()

    args = parser.parse_args(["stellar-projects", "--target", "."])
    assert args.command == "stellar-projects"

    args = parser.parse_args(["roles", "--target", "."])
    assert args.command == "roles"

    args = parser.parse_args(["miembros", "add", "--user-id", "7", "--role", "developer"])
    assert args.action == "add"
    assert args.user_id == 7
    assert args.role == "developer"

    args = parser.parse_args([
        "decision", "add",
        "--title", "Use PostgreSQL",
        "--decision", "Keep PostgreSQL as primary database",
    ])
    assert args.action == "add"
    assert args.decision_text.startswith("Keep PostgreSQL")
