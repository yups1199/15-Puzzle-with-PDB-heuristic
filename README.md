# 15-Puzzle
- Run `main.py` to play & solve 15-Puzzle.
- Solution finding requires PDB (Button is deactivated while file `pattern_database.bin` is not found)
- Solution finding may take up to 20~30 seconds with default PDB

# Pattern Database
- Press **button "build PDB"** to create file `pattern_database.bin`
  - Default : 6-6-3
  - Default Build Time : approx. 30mins
  - Default File Size : 11MB
- Modify `PATTERN_SET` at `main.py` `line 8` to modify PDB pattern
  - Default : `((1, 2, 5, 6, 9, 13),(3, 4, 7, 8, 11, 12),(10, 14, 15))`
  - ex. 5-5-5 PDB : `((1, 2, 3, 4, 5),(6, 7, 8, 9, 10),(11, 12, 13, 14, 15))`
- Delete `pattern_dabase.bin` before re-creating new PDB

# 참고
- 상세 설명 : [velog](https://velog.io/@sany19/Additive-PDB-%ED%9C%B4%EB%A6%AC%EC%8A%A4%ED%8B%B1%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%9C-15-Puzzle-Solver)
- 시연 영상 : https://www.youtube.com/watch?v=E6qiViLHMzE
