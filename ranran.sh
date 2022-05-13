install() {
  git clone https://github.com/ttranran/ranran.git
  cd ranran || exit
  python3 -m venv env
  source env/bin/activate
  cp config.toml.sample config.toml
  pip install -r requirements.txt
  cd ..
}
start() {
  cd ranran || exit
  source env/bin/activate
  nohup python3 -m ranran > runoob.log 2>&1 &
}
stop(){
  ps aux | grep "python3 -m ranran" | awk '{print $2}' | xargs kill
}


if [ $1 == "install" ]
then
   install
elif [ $1 == "start" ]
then
   start
elif [ $1 == "stop" ]
then
   start
fi