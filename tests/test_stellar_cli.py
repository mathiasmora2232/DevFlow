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


def test_discovery_and_adoption_commands_parse():
    parser = build_parser()

    args = parser.parse_args(["descubrir", "--target", ".", "--no-audit"])
    assert args.command == "descubrir"
    assert args.no_audit is True

    args = parser.parse_args(["stellar-adopt", "--target", ".", "--client-id", "12"])
    assert args.command == "stellar-adopt"
    assert args.client_id == 12

    args = parser.parse_args(["stellar-sync", "--target", ".", "--dry-run"])
    assert args.command == "stellar-sync"
    assert args.dry_run is True
