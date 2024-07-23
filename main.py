import sys, os
from src.io import VideoIO
from src.modules import Inference, Annotation, TeamClustering, BallPossession, Camera, Field, Motion

io =VideoIO()
field =Field()
clustering =TeamClustering()
ball_possession =BallPossession()
model =Inference('./model/player_detection.pt')


def main(media_path:str):
    frames =io.read(media_path)
    camera =Camera(frames[0])
    filename ='_'.join(media_path.split('/')[-1].split('.')[:-1])
    tracks =model.track_objects(frames, infer_from_stub=True, stub_path=f'out/stubs/tracking_{filename}.pkl', batch=int(io.fps))
    tracks['ball'] =model.interpolate_ball_position(tracks['ball'])
    motion =Motion(io.fps)
    player_tracks =tracks.get('players')
    clustering.set_team_color(frames[0], player_tracks[0])
    camera_movements =camera.estimate_motion(frames, read_from_stub=True, stub_path=f'out/stubs/camera_motion_{filename}.pkl')
    tracks =field.tranform_camera_view(tracks)
    tracks =camera.get_subject_position_from_camera(tracks, camera_movements)
    motion.estimate_subject_motion(tracks)
    for frame_id, player_track in enumerate(player_tracks):
        for player_id, track in player_track.items():
            team_id =clustering.get_player_team(frames[frame_id], [int(t) for t in track.get('bbox')], player_id)
            tracks['players'][frame_id][player_id]['team'] =team_id
            tracks['players'][frame_id][player_id]['team_color'] =clustering.team_colors.get(team_id)

        ball_bbox =tracks['ball'][frame_id][1].get('bbox', [])
        id_of_player_with_ball =ball_possession.get_player_with_ball(player_track, ball_bbox)
        if id_of_player_with_ball !=-1: tracks['players'][frame_id][id_of_player_with_ball]['has_ball'] =True


    annotation =Annotation(frames, tracks, ball_possession.team_ball_possesion, camera_movements =camera_movements)
    annotations =annotation.annotate_objects()
    io.write(annotations, f'out/{filename}.avi')

if __name__ == '__main__': 

    argv =sys.argv[1:]
    if not os.path.exists('out'): os.mkdir('out')
    if not os.path.exists('out/stubs'): os.mkdir('out/stubs')
    if not len(argv) ==1:
        print('[-] Usage: main.py <media_path:str>')
        sys.exit(1)
    filepath =argv[0]
    if not os.path.exists(filepath):
        print(f'[-] File {filepath} does not exist check and try again')
        sys.exit(1)
    main(filepath)
    