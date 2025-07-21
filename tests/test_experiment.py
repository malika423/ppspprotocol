"""
test_experiment.py

Verifies that experiment.main() creates a results.csv with correct headers.
"""

import scripts.experiment as experiment


def test_experiment_creates_csv_with_headers(tmp_path, monkeypatch) -> None:
    # Stub run_one to yield predictable values
    monkeypatch.setattr(experiment, "run_one", lambda p: (True, int(p * 10)))

    monkeypatch.chdir(tmp_path)
    experiment.main()

    out = tmp_path / "results.csv"
    assert out.exists()

    lines = [line.strip() for line in out.read_text().splitlines() if line.strip()]
    assert lines[0] == "steal_prob,trial,delivered,hop_count"
    assert "steal_prob,success_rate,avg_hops,std_hops" in lines
