import pytz
from spoilbuster.backend.core.node import Node
from datetime import datetime

class UserProgressNode(Node):
    def __init__(
        self, 
        input_key: list[str],  # ["user_progress_raw", "stream_start_time", "cumulative_play_time"]
        output_key: list[str], # ["final_play_time_range"]
    ):
        super().__init__(input_key, output_key)
  
    def _calculate_stream_duration(self, stream_start_time: str) -> int:
        try:
            tz = pytz.timezone("Asia/Tokyo")    # TODO: 将来的に動的に取得したい
            start_time = datetime.fromisoformat(stream_start_time).astimezone(tz)
            current_time = datetime.now(tz)
            duration = current_time - start_time
            return int(duration.total_seconds() // 3600)
        except Exception as e:
            raise ValueError(f"Invalid stream start time: {stream_start_time}") from e
    
    def _calculate_play_time_range(
        self, 
        user_progress_raw: str, 
        stream_duration: int, 
        cumulative_play_time: int
    ) -> str:
        try:
            if user_progress_raw:
                min_time, max_time = map(int, user_progress_raw.split("-"))
            elif cumulative_play_time:
                min_time, max_time = map(int, cumulative_play_time.split("-"))
            else:
                return None

            adjusted_min = min_time + stream_duration
            adjusted_max = max_time + stream_duration

            return f"{adjusted_min}-{adjusted_max}時間"
        
        except ValueError as e:
            raise ValueError(f"Invalid progress data: {user_progress_raw or cumulative_play_time}") from e
        
    def execute(self, state) -> dict:
        user_progress_raw = state.get(self.input_key[0], None)
        stream_start_time = state[self.input_key[1]]
        cumulative_play_time = state.get(self.input_key[2], None)

        stream_duration = self._calculate_stream_duration(stream_start_time)

        final_play_time_range = self._calculate_play_time_range(
            user_progress_raw, 
            stream_duration, 
            cumulative_play_time
        )

        return {
            self.output_key[0]: final_play_time_range, 
        }