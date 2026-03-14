```mermaid
flowchart LR
    A[Input: User Prefs]
    B[Load songs.csv]
    C[Build Taste Profile]
    D[Pick One Song from CSV]
    E[Score Song<br/>genre + mood + energy + tempo + valence + danceability + mode]
    F{Score passes threshold?}
    G[Keep Song]
    H[Drop Song]
    I[Deduplicate Kept Songs]
    J[Sort by Score]
    K[Output: Top K Recommendations]

    A --> C
    B --> D
    C --> E
    D --> E
    E --> F
    F -->|Yes| G
    F -->|No| H
    G --> I
    I --> J
    J --> K
```
