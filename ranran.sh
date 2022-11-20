install() {
  git clone https://github.com/yuxian158/ranran.git
  cd ranran || exit
  python3 -m venv env
  source env/bin/activate
  cp data\config\config.toml.sample data\config\config.toml
  pip install -r requirements.txt
  cd ..
}
start() {
  ps aux | grep "python3 -m ranran" | awk '{print $2}' | xargs kill
  cd ranran || exit
  source env/bin/activate
  nohup python3 -m ranran > runoob.log 2>&1 &
}
stop(){
  ps aux | grep "python3 -m ranran" | awk '{print $2}' | xargs kill
}
state(){
  ps aux | grep "python3 -m ranran"
}
pull(){
   cd ranran || exit
   git pull
}
run(){
  cd ranran || exit
  source env/bin/activate
   python3 -m ranran
}
if [ $1 == "install" ]
then
   install
elif [ $1 == "start" ]
then
   start
elif [ $1 == "stop" ]
then
   stop
elif [ $1 == "state" ]
then
   state
elif [ $1 == "run" ]
then
   run
elif [ $1 == "pull" ]
then
   pull
fi