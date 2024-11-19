
# 合并 CSV 脚本

本项目包含一个 Python 脚本，用于根据时间戳列合并多个 CSV 文件。配置非常灵活，支持不同的时间戳格式，并使用 Pixi 进行依赖管理。

## 项目结构
- **config.yaml**: 配置文件，包含输入/输出路径、跳过的行数、时间戳列等设置。
- **main.py**: 用于合并 CSV 文件的 Python 脚本。
- **requirements.txt**: 所需 Python 包列表。
- **pixi.toml**: 项目设置的 Pixi 配置文件。

## 配置文件 (`config.yaml`)
请指定以下设置：
- `input_folder`: 输入 CSV 文件所在文件夹的路径。
- `output_file`: 保存合并后 CSV 文件的路径。
- `lines_to_skip`: 每个 CSV 文件需要跳过的行数。
- `timestamp_column`: 合并后的 CSV 中时间戳列的名称。
- `timestamp_format`: 如果使用单一时间戳列，请指定其格式。
- `date_column` 和 `time_column`: 如果日期和时间分开，请指定它们的列名。
- `date_format` 和 `time_format`: 日期和时间列的格式。

## 运行项目
1. **安装 Pixi**: 使用以下命令安装 Pixi：
   ```sh
   curl -sSL https://install.pixi.rs | sh
   ```

2. **安装依赖**: 使用以下命令设置 Python 环境并安装依赖：
   ```sh
   pixi install
   ```

3. **运行脚本**: 使用配置文件运行脚本：
   ```sh
   pixi run python main.py path/to/your/config.yaml
   ```

## 注意事项
- 脚本会检查冲突的时间戳并在发现重复时通知。
- 在合并的输出文件中，时间戳列会被移动到第一列。
