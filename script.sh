cp runs/detect/train1/weights/best.pt models/best.pt
rm -R runs
dvc add models/best.pt
dvc commit
dvc push
git add models/best.pt.dvc
git commit -m 'dataset2'
gut push origins docker_train
