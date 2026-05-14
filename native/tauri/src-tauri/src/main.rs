use std::{env, fs, path::PathBuf};

fn candidate_paths(path: Option<String>) -> Vec<PathBuf> {
    let mut candidates = Vec::new();

    if let Ok(value) = env::var("AI_METER_STATUS_PATH") {
        if !value.trim().is_empty() {
            candidates.push(PathBuf::from(value));
        }
    }

    if let Some(value) = path {
        if !value.trim().is_empty() {
            candidates.push(PathBuf::from(value));
        }
    }

    candidates.push(PathBuf::from("../../runtime/status.json"));
    candidates.push(PathBuf::from("../runtime/status.json"));
    candidates.push(PathBuf::from("runtime/status.json"));

    if let Ok(cwd) = env::current_dir() {
        candidates.push(cwd.join("../../runtime/status.json"));
        candidates.push(cwd.join("../runtime/status.json"));
        candidates.push(cwd.join("runtime/status.json"));
    }

    candidates
}

#[tauri::command]
fn read_status_file(path: Option<String>) -> Result<String, String> {
    let mut tried = Vec::new();

    for candidate in candidate_paths(path) {
        tried.push(candidate.display().to_string());
        match fs::read_to_string(&candidate) {
            Ok(text) => {
                serde_json::from_str::<serde_json::Value>(&text)
                    .map_err(|error| format!("invalid JSON in {}: {}", candidate.display(), error))?;
                return Ok(text);
            }
            Err(_) => continue,
        }
    }

    Err(format!(
        "runtime status payload not found. Tried: {}",
        tried.join(", ")
    ))
}

#[tauri::command]
fn default_status_paths() -> Vec<String> {
    candidate_paths(None)
        .into_iter()
        .map(|path| path.display().to_string())
        .collect()
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![read_status_file, default_status_paths])
        .run(tauri::generate_context!())
        .expect("error while running AI Desk Meter native app");
}
