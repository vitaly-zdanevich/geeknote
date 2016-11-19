class Geeknote < Formula
  desc "Command-line client for Evernote"
  homepage 'https://github.com/jeffkowalski/geeknote'
  head 'https://github.com/jeffkowalski/geeknote.git'

  depends_on :python

  resource "websocket-client" do
    url "https://pypi.python.org/packages/a3/1e/b717151e29a70e8f212edae9aebb7812a8cae8477b52d9fe990dcaec9bbd/websocket_client-0.37.0.tar.gz"
    sha256 "678b246d816b94018af5297e72915160e2feb042e0cde1a9397f502ac3a52f41"
  end

  resource "ipaddress" do
    url "https://pypi.python.org/packages/bb/26/3b64955ff73f9e3155079b9ed31812afdfa5333b5c76387454d651ef593a/ipaddress-1.0.17.tar.gz"
    sha256 "3a21c5a15f433710aaa26f1ae174b615973a25182006ae7f9c26de151cd51716"
  end

  resource "orderedmultidict" do
    url "https://pypi.python.org/packages/10/a5/a9596229782ffcb465f288588dff39ccd7f64fc453d64f75f5ef442315a8/orderedmultidict-0.7.11.tar.gz"
    sha256 "dc2320ca694d90dca4ecc8b9c5fdf71ca61d6c079d6feb085ef8d41585419a36"
  end

  resource "oauth2" do
    url "https://pypi.python.org/packages/source/o/oauth2/oauth2-1.9.0.post1.tar.gz"
    sha256 "c006a85e7c60107c7cc6da1b184b5c719f6dd7202098196dfa6e55df669b59bf"
  end

  resource "httplib2" do
    url "https://pypi.python.org/packages/source/h/httplib2/httplib2-0.9.2.tar.gz"
    sha256 "c3aba1c9539711551f4d83e857b316b5134a1c4ddce98a875b7027be7dd6d988"
  end

  resource "evernote" do
    url "https://pypi.python.org/packages/source/e/evernote/evernote-1.25.1.tar.gz"
    sha256 "6f9838307e28819954c18b92eed5616b91aa4b2230c2ee325f44d97cde9d12a8"
  end

  resource "html2text" do
    url "https://pypi.python.org/packages/source/h/html2text/html2text-2016.1.8.tar.gz"
    sha256 "088046f9b126761ff7e3380064d4792279766abaa5722d0dd765d011cf0bb079"
  end

  resource "SQLAlchemy" do
    url "https://pypi.python.org/packages/source/S/SQLAlchemy/SQLAlchemy-1.0.12.tar.gz"
    sha256 "6679e20eae780b67ba136a4a76f83bb264debaac2542beefe02069d0206518d1"
  end

  resource "markdown2" do
    url "https://pypi.python.org/packages/source/m/markdown2/markdown2-2.3.0.zip"
    sha256 "c8e29ba47a0e408bb92df75d5c6361c84268c54c5320d53ffd4961c546f77f1c"
  end

  resource "beautifulsoup4" do
    url "https://pypi.python.org/packages/source/b/beautifulsoup4/beautifulsoup4-4.4.1.tar.gz"
    sha256 "87d4013d0625d4789a4f56b8d79a04d5ce6db1152bb65f1d39744f7709a366b4"
  end

  resource "thrift" do
    url "https://pypi.python.org/packages/source/t/thrift/thrift-0.9.3.tar.gz"
    sha256 "dfbc3d3bd19d396718dab05abaf46d93ae8005e2df798ef02e32793cd963877e"
  end

  resource "future" do
    url "https://pypi.python.org/packages/5a/f4/99abde815842bc6e97d5a7806ad51236630da14ca2f3b1fce94c0bb94d3d/future-0.15.2.tar.gz"
    sha256 "3d3b193f20ca62ba7d8782589922878820d0a023b885882deec830adbf639b97"
  end

  # for proxyenv
  resource "docker-py" do
    url "https://pypi.python.org/packages/d7/32/1e6be8c9ebc7d02fe74cb1a050008bc9d7e2eb9219f5d5e257648166e275/docker-py-1.9.0.tar.gz"
    sha256 "6dc6b914a745786d97817bf35bfc1559834c08517c119f846acdfda9cc7f6d7e"
  end

  # for proxyenv
  resource "htpasswd" do
    url "https://pypi.python.org/packages/b9/2f/8b76f8b77125b75c3532966f3291f9e8787268be65fc4c9694887cba9375/htpasswd-2.3.tar.gz"
    sha256 "565f0b647a32549c663ccfddd1f501891daaf29242bbc6174bdd448120383e3d"
  end

  resource "proxyenv" do
    url "https://pypi.python.org/packages/69/98/46baccf9ce353828726e0d302dad201e634fe4b50f6f61891f0721f40789/proxyenv-0.5.1.tar.gz"
    sha256 "e73caf8b063b7fbfb93b67e725a71469768262a9dddb4d9dfb79bb1e84cab4b9"
  end

  resource "lxml" do
    url "https://pypi.python.org/packages/4f/3f/cf6daac551fc36cddafa1a71ed48ea5fd642e5feabd3a0d83b8c3dfd0cb4/lxml-3.6.4.tar.gz"
    sha256 "61d5d3e00b5821e6cda099b3b4ccfea4527bf7c595e0fb3a7a760490cedd6172"
  end

  def install
    ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"
    resources.each do |r|
      r.stage do
        system "python", *Language::Python.setup_install_args(libexec/"vendor")
      end
    end

    ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python2.7/site-packages"
    system "python", *Language::Python.setup_install_args(prefix)

    bash_completion.install "completion/bash_completion/_geeknote" => "geeknote"
    zsh_completion.install "completion/zsh_completion/_geeknote" => "_geeknote"

    bin.env_script_all_files(libexec/"bin", :PYTHONPATH => ENV["PYTHONPATH"])
  end

  test do
    system "py.test"
  end
end
